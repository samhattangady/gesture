#!/usr/bin/env python
# Consists of function to return the centroid of the largest contour of given colour thresholds
import numpy as np
import cv2

kernel = np.zeros((5,5),np.uint8)

# Function. First isolates the finger pased on HSV limits. Morphology functions are to remove noise and make it clearer
# We then find the contours of the shape we are following. Draw the contours, as well as draw a filled circle in the cetroid
def fingerTrack(hsv, finger, frame):
	fingerMask = cv2.inRange(hsv, np.array(finger[0]), np.array(finger[1]))
	finger = cv2.bitwise_and(frame, frame, mask = fingerMask)
	finger = cv2.morphologyEx(finger, cv2.MORPH_OPEN, kernel)
	finger = cv2.dilate(finger, kernel, iterations=2)
	fingerCanny = cv2.Canny(finger, 100, 200)
	_, contours, heirarchy = cv2.findContours(fingerCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	# To find the centroid of the largest contour  
	largestContourArea = 0
	centroidExists = False # This is because if there is no tracked object on screen, error will cause script to crash
	for cnt in contours:
		M = cv2.moments(cnt)
		if M['m00'] != 0 and M['m00'] > largestContourArea:		
			fingerX = int(M['m10']/M['m00'])
			fingerY = int(M['m01']/M['m00'])
			largestContourArea = M['m00']
			centroidExists = True
	if centroidExists:
		fingerCoord = (fingerX, fingerY)
	else:
		fingerCoord = None 

	return fingerCoord


