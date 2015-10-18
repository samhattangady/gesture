import numpy as np
import cv2

# Declaring list of colours of possible fingers in HSV lower and upper limit format
# If you need to add to this list, use colourPicker and isolate the coloured element that you need.
pink = [[148,170,22],[179,255,255]]
green = [[41,129,66],[81,255,255]]

# Declaring a list of colours for contour lines in BRG format
redContours = (000,000,255)
greenContours = (000,255,000)
blueContours = (255,000,000)

# Select colour for each finger
indexColour= pink
thumbColour= green

# Setting kernel for morphology operations
kernel = np.ones((5,5), np.uint8)

# Starting video capture
cap = cv2.VideoCapture(0)

# Function. First isolates the finger pased on HSV limits. Morphology functions are to remove noise and make it clearer
# We then find the contours of the shape we are following. Draw the contours, as well as draw a filled circle in the cetroid
def fingerTrack(hsv,finger,frame,contourColour):
	fingerMask = cv2.inRange(hsv, np.array(finger[0]), np.array(finger[1]))
	resFinger = cv2.bitwise_and(frame, frame, mask = fingerMask)
	resFinger = cv2.morphologyEx(resFinger, cv2.MORPH_OPEN, kernel)
	resFinger = cv2.dilate(resFinger, kernel, iterations=4)
	resFingerCanny = cv2.Canny(resFinger, 100, 200)
	_, contours, heirarchy = cv2.findContours(resFingerCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(resFinger, contours, -1, contourColour, 1)
	
	# To find the centroid of the contoured shape and draw a circle. Send only one.
	tracked = 0;
	for cnt in contours:
		M = cv2.moments(cnt)
		if M['m00'] != 0 and tracked == 0:		
			fingerX = int(M['m10']/M['m00'])
			fingerY = int(M['m01']/M['m00'])
			resFinger = cv2.circle(resFinger,(fingerX,fingerY), 7, contourColour, -1) 
			tracked = tracked+1

	return resFinger

# Loop to be run every frame
while(1):

	# We start by reading every frame from the video input. We flip it horizontally, convert to HSV, and blur it	
	_, frame = cap.read()
	frame = cv2.flip(frame,1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (5,5),0)

	# Send the fingers to the function fingerTrack based on their colours, and the colour of contours/centroid dots that we want
	index = fingerTrack(hsv, indexColour, frame, redContours)
	thumb = fingerTrack(hsv, thumbColour, frame, greenContours)
 	
	# Add the two resultant
	res = cv2.add(thumb,index)

	# Display image and quit when 'Esc' key is pressed
	cv2.imshow ('Tracker',res)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
