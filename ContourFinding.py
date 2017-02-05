import cv2, copy
import numpy as np
import Printing
import config


numTargets = 2

sizeWeight = 1
ratioWeight = 10
rotationWeight = 0.1
rectangularWeight = 3
areaWeight = 5
quadWeight = 50
weights = np.array([sizeWeight, ratioWeight, rotationWeight, rectangularWeight, areaWeight, quadWeight])

maxArea, minArea = 150000, 4000

def filterContours(contours):
	numContours = len(contours)
	# if debug:
	# 	print "Number of contours: {}".format(numContours)
	if numContours > 1:
		# Find 2 largest contours.
		largest_contour, second_largest_contour, largest_area, second_largest_area = None, None, 0, 0
		for i in range(numContours):
			temp_area = cv2.contourArea(contours[i], False)
			if temp_area > second_largest_area:
				if temp_area > largest_area:
					largest_contour, second_largest_contour = contours[i], largest_contour
					largest_area, second_largest_area = temp_area, largest_area
				else:
					second_largest_contour = contours[i]
					second_largest_area = temp_area
		return largest_contour, second_largest_contour
	else:
		return contours

def filterContoursFancy(contours, image=None):
	numContours = len(contours)
	print contours[0]
	areas = np.array([cv2.contourArea(contour) for contour in contours])

	boundingRects = [cv2.boundingRect(contour) for contour in contours]
	widths, heights, positions = boundingInfo(boundingRects)

	rotatedRects = [cv2.minAreaRect(contour) for contour in contours]
	rotatedBoxes = [np.int0(cv2.cv.BoxPoints(rect)) for rect in rotatedRects]
	print rotatedRects[0]
	print rotatedBoxes[0]
	rotatedAreas = [cv2.contourArea(box) for box in rotatedBoxes]

	sizeScores = [size(area)for area in areas]
	ratioScores = ratios(widths, heights)
	rotationScores = [rotation(rect) for rect in rotatedRects]
	rectangularScores = [distToPolygon(contour, poly) for contour,poly in zip(contours, rotatedBoxes)]
	areaScores = polygonAreaDiff(areas, rotatedAreas)
	quadScores = [Quadrify(contour) for contour in contours]
	# quadScores = [distToPolygon(contour, quad) for contour,quad in zip(contour,quad)]

	rectangularScores = np.divide(rectangularScores, widths)

	scores = np.array([sizeScores, ratioScores, rotationScores, rectangularScores, areaScores, quadScores])
	contourScores = np.dot(weights, scores)

	correctInds, incorrectInds = sortedInds(contourScores)
	correctContours = np.array(contours)[correctInds]

	if config.debug:
		print "ratio, rotation, rectangular, area, quad"
		print "Weights:", weights
		print "Scores: ", contourScores
		print np.average(scores, axis=1)
		if len(incorrectInds) != 0:
			print "AVG, WORST", test(scores, correctInds, incorrectInds)

	if config.extra_debug:
		for i in range(numContours):
			img = copy.deepcopy(image)
			print "CONTOUR " + str(i)
			print np.multiply(scores[:, i], weights) #newWeights
			print contourScores[i]
			Printing.drawImage(img, contours[:i] + contours[i+1:], contours[i], False)
			Printing.display(img, "contour " + str(i), defaultSize=True)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	return correctContours

def sortedInds(scores):
	sortedScoresIndices = scores.argsort()
	return sortedScoresIndices[:numTargets], sortedScoresIndices[numTargets:]

def test(scores, correctInds, incorrectInds):
	correct = scores[:, correctInds]
	incorrect = scores[:, incorrectInds]

	worstCorrect = np.amax(correct, axis=1)
	bestIncorrect = np.amin(incorrect, axis=1)
	worstdiffs = np.divide(bestIncorrect+0.00001, worstCorrect+0.00001) - 1

	avgCorrect = np.average(correct, axis=1)
	avgIncorrect = np.average(incorrect, axis=1)
	avgdiffs = np.divide(avgIncorrect+0.00001, avgCorrect+0.00001) - 1

	return avgdiffs, worstdiffs

def boundingInfo(rects):
	rects = np.array(rects)
	widths = rects[:,2]
	heights = rects[:,3]
	positions = rects[:,:2]
	return widths, heights, positions

def rotatedInfo(rects):
	widths, heights = np.array([]), np.array([])
	for rect in rects:
		widths.append(rect[1][0])
		heights.append(rect[1][1])
		# center = rect[0] + rotate(rect[1] by angles)
	return widths, heights

def distToPolygon(contour, polygon):
	tests = [cv2.pointPolygonTest(polygon, (point[0][0], point[0][1]), True) for point in contour]
	return np.average(np.absolute(tests))
	# (point[0][0], point[0][1]) replace with point?

def rotation(rotatedRect):
	angle = rotatedRect[2]
	rotation = np.minimum(np.add(angle, 90), np.negative(angle)) #That's just how minarearect works
	return rotation

def size(area):
	# DONT DO MAYBE
	# Too large bad, too small bad
	diff = 1
	if area > maxArea:
		diff = np.divide(area, maxArea)
	if area < minArea:
		diff = np.divide(minArea, area)
	return np.log(diff)


# The dimensions of the tape is 2 x 5 inches, so expect ed height is 1.5 times the width	
def ratios(widths, heights):
	ratios = np.divide(np.true_divide(heights, widths), 1.5)
	return np.absolute(np.log(ratios))
	# Subtract the difference from what is expected from that contour's score
	# contourScores[i] -= abs(heights[i] - widths[i]*1.5)
	# Log instead of subtraction so it scales

# def multipleRatioTest(rectOne, rectTwo):
#	Same width (same height, stuff)
#	https://wpilib.screenstepslive.com/s/4485/m/24194/l/683625-processing-images-from-the-2017-frc-game maybe
#	Pairs all contours with each other, and checks that the bounding rectangle around
#	both of them is the dimensions that it should be

def polygonAreaDiff(areas, polyAreas):
	ratios = np.divide(polyAreas, areas)
	return np.absolute(np.log(ratios))
	# cv2.contourArea(poly)


def Quadrify(contour):
	epsilon = 10
	for i in range(1,10):
		quad = cv2.approxPolyDP(contour, epsilon, True)
		length = len(quad)
		randomVar = np.random.random()
		epsilon = np.multiply(epsilon, np.true_divide(np.add(length, randomVar), np.add(4, randomVar)))
		# print epsilon, length
		if length == 4:
			return np.multiply(i,0.01)
	return 1


# NOT OF VARIABLE SIZE
def fitPattern(image, pattern, method=cv2.TM_SQDIFF):
	location, patternSize = None, None
	scores = cv2.matchTemplate(image, pattern, method)
	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(scores)
	if method  == cv2.TM_SQDIFF or method == cv2.TM_SQDIFF_NORMED:
		location = minLoc
	else:
		location = maxLoc
	center = np.add(location, patternSize)
	return center


# Parallelograms everywhere. Otherwise quads or minarearectangle
# Perimeter
# What about spike? Test image, test scores. How to get around it
# Paired or triplet contours
# Run approxPoly once and record num sides?

# read about:
# convexity defects
# floodfill
