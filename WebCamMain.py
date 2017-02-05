"""
Simple skeleton program for running an OpenCV Falsepeline generated by GRIP and using NetworkTables to send data.
Users need to:
1. Import the generated GRIP Falsepeline, which should be generated in the same directory as this file.
2. Set the network table server IP. This is usually the robots address (roborio-TEAM-frc.local) or localhost
3. Handle putting the generated code into NetworkTables
"""

import cv2
import numpy as np
from ContourFinding import filterContours #, filterContoursFancy
from SpikeFinding import findCenterandDist
import WebCam
import GripRunner
from config import *
import NetworkTabling
if debug:
	import Printing

def main():
	WebCam.set(exposure=exposure, resolution=resolution, contrast=contrast, gain=gain)
	if not edited:
		GripRunner.editCode()
	if display:
		cv2.namedWindow("Contours Found")
	frameNum = 1
	while True:
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		targets = filterContours(contours) # To be edited if the last filter is changed in case of algorithmic changes. 
		center, distance = findCenterandDist(targets) #if 2, join and find center, if 1, return val, if 0 return input. if adjustCoords:	center[0] -= halfWidth
		# if debug:
		# 	Printing.printResults(contours, center, distance)
		if save or display:
			Printing.drawImage(image, contours, targets, center)
			if save:
				Printing.save(image)
			if display:
				Printing.display(image, defaultSize=True)
		try:
			NetworkTabling.publishToTables(center, distance=distance, frameNum=frameNum)
		except Exception as error:
			if debug:
				print error
				# print "The networktables are mean to us"
		frameNum += 1
		cv2.waitKey(500)
	if display:
		cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
