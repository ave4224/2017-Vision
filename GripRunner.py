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

sample = True
pi = False
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
			largest_contour, second_largest_countour = largest_contour, second_largest_countour
			largest_area, second_largest_area = second_largest_area, largest_area
		for i in range(2, numContours):
			temp_area = cv2.contourArea(contours[i], False)
			if (temp_area > second_largest_area):
				second_largest_contour = contours[i]
				second_largest_area = temp_area
				if second_largest_area > largest_area:
					largest_contour, second_largest_countour = largest_contour, second_largest_countour
					largest_area, second_largest_area = second_largest_area, largest_area
        totalContour = np.concatenate(largest_contour, second_largest_contour)
        x, y, w, h = cv2.boundingRect(totalContour)
        return (x,y)
    elif numContours == 1:
        x, y, w, h = cv2.boundingRect(contour)
        return (x,y)
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

    #######################
    # NetworkTables stuff #
    #######################

    sd = NetworkTables.getTable("SmartDashboard")
    try:
        # print('valueFromSmartDashboard:', sd.getNumber('valueFromSmartDashboard'))
        pipeline.calibrate(hsv_threshold_hue=sd.getNumber('hsv_threshold_hue'), hsv_threshold_saturation=sd.getNumber('hsv_threshold_value'), hsv_threshold_saturation=sd.getNumber('hsv_threshold_value'))
    except KeyError:
        # print('valueFromSmartDashboard: N/A')

    sd.putNumber('centerX', centerX)
    sd.putNumber('centerY', centerY)
    
    # ---------------------

    # TODO: Users need to implement this.
    # Useful for converting OpenCV objects (e.g. contours) to something NetworkTables can understand.
    pass


def main():
    # NetworkTable.setTeam('4904')
    # NetworkTable.initialize()
    pipeline = GripPipeline()
    # cap = cv2.VideoCapture(0)
    if sample:
        image = cv2.imread("TapeTest.jpg")
        pipeline.process(image)  # TODO add extra parameters if the pipeline takes more than just a single image
        extra_processing(pipeline)

    if pi:
        while True:
            image = camera.getImage()
            pipeline.process(image)  # TODO add extra parameters if the pipeline takes more than just a single image
            extra_processing(pipeline)


if __name__ == '__main__':
    main()
