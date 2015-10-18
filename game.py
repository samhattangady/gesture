import pygame as pg
import numpy as np
import cv2
import colours as clr
import track

# Setting colours for fingers
thumb = clr.pinkHSV
index = clr.greenHSV
background = clr.blueBeige
upperClaw = clr.blueBeige2
lowerClaw = clr.blueBeige3

clock = pg.time.Clock()

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
	hsv = cv2.GaussianBlur(hsv, (5,5), 0)

	# Calling the function to find the coordinates of the trackers attached to the fingers
	thumbCoord = track.fingerTrack (hsv, thumb, frame)	
	indexCoord = track.fingerTrack (hsv, index, frame)

	if thumbCoord != None:
		pg.draw.rect(screen, lowerClaw, pg.Rect((thumbCoord[0], thumbCoord[1], 45, 15)))
	if indexCoord != None:		
		pg.draw.rect(screen, upperClaw, pg.Rect((indexCoord[0], indexCoord[1], 45, 15)))

	pg.display.flip()
	clock.tick(60)
