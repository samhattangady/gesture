#!/usr/bin/env python
# Displays the tracked fingers as circles on the screen

import numpy as np
import cv2
import colours as clr

# Select colour for each finger
indexColour= clr.pink
thumbColour= clr.green

# Setting kernel for morphology operations
kernel = np.ones((5,5), np.uint8)

# Starting video capture
cap = cv2.VideoCapture(0)
_,temp = cap.read()
resolution = temp.shape 
print resolution
# Function. First isolates the finger pased on HSV limits. Morphology functions are to remove noise and make it clearer
# We then find the contours of the shape we are following. Draw the contours, as well as draw a filled circle in the cetroid
def fingerTrack(hsv, finger, frame, centroidColour, screen):
	fingerMask = cv2.inRange(hsv, np.array(finger[0]), np.array(finger[1]))
	finger = cv2.bitwise_and(frame, frame, mask = fingerMask)
	finger = cv2.morphologyEx(finger, cv2.MORPH_OPEN, kernel)
	finger = cv2.dilate(finger, kernel, iterations=4)
	fingerCanny = cv2.Canny(finger, 100, 200)
	_, contours, heirarchy = cv2.findContours(fingerCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	# To find the centroid of the largest contour  
	largestContourArea = 0
	centroidExists = False # This is because if there is no tracked object on screen, script will close
	for cnt in contours:
		M = cv2.moments(cnt)
		if M['m00'] != 0 and M['m00'] > largestContourArea:		
			fingerX = int(M['m10']/M['m00'])
			fingerY = int(M['m01']/M['m00'])
			largestContourArea = M['m00']
			centroidExists = True
	if centroidExists:
		finger = cv2.circle(screen,(fingerX,fingerY), 7, centroidColour, -1)
	else:
		finger = screen

	return finger

# Loop to be run every frame
while(1):

	# We start by reading every frame from the video input. We flip it horizontally, convert to HSV, and blur it	
	_, frame = cap.read()
	frame = cv2.flip(frame,1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (5,5),0)
	screen = np.zeros(resolution, np.uint8)

	# Send the fingers to the function fingerTrack based on their colours, and the colour of contours/centroid dots that we want
	index = fingerTrack(hsv, indexColour, frame, clr.redContours, screen)
	thumb = fingerTrack(hsv, thumbColour, frame, clr.greenContours, screen)
 	
	# Draw circles at the tracked coordinates
	res = cv2.add(thumb,index)

	# Display image and quit when 'Esc' key is pressed
	cv2.imshow ('Tracker',res)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
