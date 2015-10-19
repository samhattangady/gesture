import numpy as np
import cv2
import colours

# Select colour for each finger
indexColour= colours.pinkHSV
thumbColour= colours.yellowHSV
ringColour = colours.blueHSV
#middleColour=colours.greenHSV
#pinkyColour = colours.orangeHSV

# Setting kernel for morphology operations
kernel = np.ones((5,5), np.uint8)

# Starting video capture
cap = cv2.VideoCapture(0)

# Function. First isolates the finger pased on HSV limits. Morphology functions are to remove noise and make it clearer
# We then find the contours of the shape we are following. Draw the contours, as well as draw a filled circle in the cetroid
def fingerTrack(hsv,finger,frame,contourColour):
	fingerMask = cv2.inRange(hsv, np.array(finger[0]), np.array(finger[1]))
	finger = cv2.bitwise_and(frame, frame, mask = fingerMask)
	finger = cv2.morphologyEx(finger, cv2.MORPH_OPEN, kernel)
	finger = cv2.dilate(finger, kernel, iterations=4)
	fingerCanny = cv2.Canny(finger, 100, 200)
	_, contours, heirarchy = cv2.findContours(fingerCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(finger, contours, -1, contourColour, 1)
	
	# To find the centroid of the largest contour and draw a circle. 
	largestContourArea = 0
	drawCentroid = False # This is because if there is no tracked object on screen, script will close
	for cnt in contours:
		M = cv2.moments(cnt)
		if M['m00'] != 0 and M['m00'] > largestContourArea:		
			fingerX = int(M['m10']/M['m00'])
			fingerY = int(M['m01']/M['m00'])
			largestContourArea = M['m00']
			drawCentroid = True
	if drawCentroid:
		resFinger = cv2.circle(finger,(fingerX,fingerY), 7, contourColour, -1) 

	return finger

# Loop to be run every frame
while(1):

	# We start by reading every frame from the video input. We flip it horizontally, convert to HSV, and blur it	
	_, frame = cap.read()
	frame = cv2.flip(frame,1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (5,5),0)

	# Send the fingers to the function fingerTrack based on their colours, and the colour of contours/centroid dots that we want
	index = fingerTrack(hsv, indexColour, frame, colours.redBGR)
	thumb = fingerTrack(hsv, thumbColour, frame, colours.greenBGR)
	ring = fingerTrack (hsv, ringColour, frame, colours.greenBGR)
#	middle =fingerTrack(hsv,middleColour, frame, colours.redBGR)
#	pinky = fingerTrack(hsv, pinkyColour, frame, colours.greenBGR) 	

	# Add the two resultant
	res = cv2.add(thumb,index)

	# Display image and quit when 'Esc' key is pressed
	cv2.imshow ('Tracker',res)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
