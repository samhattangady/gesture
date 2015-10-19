import pygame as pg
import numpy as np
import cv2
import colours as clr
import track

# Setting colours for fingers
thumb = clr.yellowHSV
index = clr.pinkHSV
background = clr.blueBeige
upperClaw = clr.blueBeige2
lowerClaw = clr.blueBeige3

clock = pg.time.Clock()

# Setting constants for game objects
clawWidth = 45
clawHeight = 15
blurSize = 5
speed = 1
thumbCoord = None # Initializing variables, because we need to store the past values.
indexCoord = None
 
# Starting camera, as well as finding the dimensions
cap = cv2.VideoCapture(0)
_, temp = cap.read()
resolution = temp.shape
y,x,depth = resolution # temp.shape returns in rows and coloumns. So rows = y, coloumns = x

pg.init()
screen = pg.display.set_mode((x, y))
done = False

while not done:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			done = True
	
	screen.fill(background)
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (blurSize, blurSize), 0)

	# Calling the function to find the coordinates of the trackers attached to the fingers
	if thumbCoord != None:
		thumbPrev = thumbCoord
	if indexCoord != None:
		indexPrev = indexCoord
	
	thumbCoord = track.fingerTrack (hsv, thumb, frame)	
	indexCoord = track.fingerTrack (hsv, index, frame)

	if thumbCoord != None:
		pg.draw.rect(screen, lowerClaw, pg.Rect((thumbCoord[0]+(clawWidth/2), thumbCoord[1]+(clawHeight/2), clawWidth, clawHeight)))
	if indexCoord != None:		
		pg.draw.rect(screen, upperClaw, pg.Rect((indexCoord[0]+(clawWidth/2), indexCoord[1]+(clawHeight/2), clawWidth, clawHeight)))

	pg.display.flip()
#	clock.tick(60)
