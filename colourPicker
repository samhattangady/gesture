# This is used to find the HSV limits of any objects. Just need to drag the sliders forward and back until the object that you need is in white 
# The 'Picker' window shows what the camera sees, unfiltered. 'Mask' window varies with changes in HSV sliders.
# For now, you will have to manually note down the HSV upper and lower values. Later on, maybe an export functionality can be included. 

import numpy as np
import cv2

def nothing(x):
	pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('Picker')
cv2.createTrackbar('LowerHue','Picker',000,179,nothing)
cv2.createTrackbar('UpperHue','Picker',179,179,nothing)
cv2.createTrackbar('LowerSat','Picker',000,255,nothing)
cv2.createTrackbar('UpperSat','Picker',255,255,nothing)
cv2.createTrackbar('LowerVal','Picker',000,255,nothing)
cv2.createTrackbar('UpperVal','Picker',255,255,nothing)

while (1):
	_, frame = cap.read()
	hsv = cv2.cvtColor (frame,cv2.COLOR_BGR2HSV)

	lower = np.array([cv2.getTrackbarPos('LowerHue','Picker'),cv2.getTrackbarPos('LowerSat','Picker'),cv2.getTrackbarPos('LowerVal','Picker')])
	upper = np.array([cv2.getTrackbarPos('UpperHue','Picker'),cv2.getTrackbarPos('UpperSat','Picker'),cv2.getTrackbarPos('UpperVal','Picker')])

	mask = cv2.inRange (hsv,lower,upper)
	res = cv2.bitwise_and(frame,frame, mask= mask)
	
	cv2.imshow('Picker',res)
	cv2.imshow('Mask',mask)

	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
