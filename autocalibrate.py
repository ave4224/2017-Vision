import numpy as np
import GripRunner, Printing, WebCam, config
import cv2, time

minExposure = 3
maxExposure = 1000
resolutionArea = 600000
maxArea = resolutionArea/4
targetAverageValue = 30
averageValueThreshold = 20
numTests = 5
# test image max area is 58106.0

# image = cv2.imread('TestImages/Cancer.jpg')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# value = cv2.split(image)[2]
# # value = np.array([image[:,:,2]])
# average = cv2.mean(value)
# print average

def autocalibrate():
	print "Calibrating WebCam... (may not work)"
	currentTime = time.clock()
	exposure = WebCam.getExposure()
	newTime = time.clock()
	getExposureTime = np.subtract(newTime, currentTime)
	currentTime = time.clock()
	brightIters = []
	runTimes = []
	restTimes = []
	for i in range(10):
		image = WebCam.getImage()
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		value = cv2.split(image)[2]
		average = cv2.mean(value)[0]
		if config.display:
			Printing.display(image)
		if np.absolute(np.subtract(average, targetAverageValue)) < averageValueThreshold:
			break
		scaleBy = np.divide(targetAverageValue, average)
		exposure = np.minimum(np.maximum(np.multiply(exposure, scaleBy), minExposure), maxExposure)
		WebCam.set(exposure=exposure)

		newTime = time.clock()
		brightIters += [np.subtract(newTime, currentTime)]
		currentTime = time.clock()

	numGoodFrames = 0
	for i in range(20):
		image = WebCam.getImage()
		tempTime = time.clock()
		contours = GripRunner.run(image)
		currentTime = time.clock()
		runTimes += [np.subtract(currentTime, tempTime)]
		numContours = len(contours)
		# print numContours, exposure, WebCam.getExposure()
		if numContours > 0:
			if tooLarge(contours):
				exposure = np.divide(exposure, 10)
		if numContours == 2:
			numGoodFrames += 1
			if numGoodFrames == numTests:
				# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
				# value = cv2.split(image)[2]
				# average = cv2.mean(value)[0]
				# print average
				break
				# return True
		else:
			numGoodFrames = 0
		randomVar = np.random.random_sample()
		scaleBy = np.true_divide(2+randomVar, numContours+randomVar)
		exposure = np.minimum(np.maximum(np.multiply(exposure, scaleBy), minExposure), maxExposure)
		WebCam.set(exposure=exposure)
		restTimes += [np.subtract(time.clock(),currentTime)]
		if config.display:
			Printing.drawContours(image, contours)
			Printing.display(image)
	print "getExposureTime", getExposureTime
	print "bright", np.average(brightIters), brightIters
	print "run", np.average(runTimes), runTimes
	print "rest", np.average(restTimes), restTimes
	return False


def tooLarge(contours):
	areas = [cv2.contourArea(contour, False) for contour in contours]
	largest = np.amax(areas)
	if largest > maxArea:
		return True
	else:
		return False


def displace():
	WebCam.set(exposure=1000)

# 	shutter_speed = WebCam.getShutterSpeed()

# 		shutter_speed = np.multiply(shutter_speed, np.true_divide(numContours+randomVar, 2+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
# 		WebCam.set(shutter_speed=shutter_speed)
 
# if numContours == 2:
# 			for i in range(numTests):
# 				image = WebCam.getImage()
# 				contours = GripRunner.run(image)
# 				numContours = len(contours)
# 				if numContours != 2:
# 					break
# 			else:
# 				break

if __name__ == '__main__':
	autocalibrate()