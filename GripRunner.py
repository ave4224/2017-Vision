"""
Simple skeleton program for running an OpenCV pipeline generated by GRIP and using NetworkTables to send data.
Users need to:
1. Import the generated GRIP pipeline, which should be generated in the same directory as this file.
2. Set the network table server IP. This is usually the robots address (roborio-TEAM-frc.local) or localhost
3. Handle putting the generated code into NetworkTables
"""

import cv2
import numpy as np
# from networktables import NetworkTable
from grip import GripPipeline  # TODO change the default module and class, if needed
from networktables import NetworkTables

sample = False
pi = True
if pi:
	import camera

def findCenter(contours):
	numContours = len(contours)
	if numContours > 1:
		# Find 2 largest contours.
		largest_contour = contours[0]
		second_largest_contour = contours[1]
		largest_area = cv2.contourArea(contours[0], False)
		second_largest_area = cv2.contourArea(contours[1], False)
		if second_largest_area > largest_area:
			largest_contour, second_largest_contour = largest_contour, second_largest_contour
			largest_area, second_largest_area = second_largest_area, largest_area
		for i in range(2, numContours):
			temp_area = cv2.contourArea(contours[i], False)
			if (temp_area > second_largest_area):
				second_largest_contour = contours[i]
				second_largest_area = temp_area
				if second_largest_area > largest_area:
					largest_contour, second_largest_contour = largest_contour, second_largest_contour
					largest_area, second_largest_area = second_largest_area, largest_area
		totalContour = np.concatenate((largest_contour, second_largest_contour))
		x, y, w, h = cv2.boundingRect(totalContour)
		x1, y1, w1, h1 = cv2.boundingRect(largest_contour)
		x2, y2, w2, h2 = cv2.boundingRect(second_largest_contour)
		img = cv2.imread("GearTest.png")

		# Show the rectangles:
		# cv2.rectangle(img, (x, y), (x+w,y+h), (255,0,0))
		# cv2.rectangle(img, (x, y), (x+5,y+5), (255,255,0))
		# cv2.rectangle(img, (x1, y1), (x1+w1,y1+h1), (2,2,255))
		# cv2.rectangle(img, (x2, y2), (x2+w1,y2+h2), (255,2,255))

		# cv2.imshow("sdf", img)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

		return (x+w/2,y+h/2)
	elif numContours == 1:
		x, y, w, h = cv2.boundingRect(contours[0])
		# img = cv2.imread("GearTest.png")
		# cv2.rectangle(img, (x, y), (x+w,y+h), (255,0,0))
		# cv2.rectangle(img, (x, y), (x+5,y+5), (255,255,0))
		# cv2.imshow("sdf", img)
		return (x+w/2,y+h/2)
	else:
		return (0,0)


def extra_processing(pipeline):
	"""
	Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
	:param pipeline: the pipeline that just processed an image
	:return: None

	"""
	targets = pipeline.filter_contours_output
	center = findCenter(targets)
	print center
	#######################
	# NetworkTables stuff #
	#######################
	sd = NetworkTables.getTable("SmartDashboard")
	try:
		pass
		# print('valueFromSmartDashboard:', sd.getNumber('valueFromSmartDashboard'))
		# pipeline.calibrate(hsv_threshold_hue=sd.getNumber('hsv_threshold_hue'), hsv_threshold_saturation=sd.getNumber('hsv_threshold_value'), hsv_threshold_value=sd.getNumber('hsv_threshold_value'))
	except KeyError:
		# print('valueFromSmartDashboard: N/A')
		pass

	sd.putNumber('centerX', center[0])
	sd.putNumber('centerY', center[1])


	# TODO: Users need to implement this.
	# Useful for converting OpenCV objects (e.g. contours) to something NetworkTables can understand.
	pass


def main():
	# NetworkTable.setTeam('4904')
	# NetworkTable.initialize()
	pipeline = GripPipeline()
	ip = "10.1.128.47"
	NetworkTables.initialize(server=ip)
	# cap = cv2.VideoCapture(0)
	if sample:
		image = cv2.imread("GearTest.png")
		pipeline.process(image)  # TODO add extra parameters if the pipeline takes more than just a single image
		extra_processing(pipeline)

	if pi:
		while True:
			image = camera.getImage()
			pipeline.process(image)  # TODO add extra parameters if the pipeline takes more than just a single image
			extra_processing(pipeline)


if __name__ == '__main__':
	main()
