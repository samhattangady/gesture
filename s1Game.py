# First stage of game. Only the moving claws has been implemented

import pygame as pg
import numpy as np
import cv2
import colours as clr
import track
import collide

# Setting colours for fingers
thumb = clr.pinkHSV
index = clr.greenHSV
background = clr.blueBeige
upperClaw = clr.blueBeige2
lowerClaw = clr.blueBeige3

clock = pg.time.Clock()

# Setting constants for game objects
clawWidth = 45
clawHeight = 15
blurSize = 5
speed = 1
thumbCoord= indexCoord= thumbRect= indexRect = None # Initializing variables, because we need to store the past values.

 
# Starting camera, as well as finding the dimensions
cap = cv2.VideoCapture(0)
_, temp = cap.read()
resolution = temp.shape
y,x,depth = resolution # temp.shape returns in rows and coloumns. So rows = y, coloumns = x

pg.init()
screen = pg.display.set_mode((x, y))
exitGame = False

# Function to convert coordinates to pg.Rect
def coordToRect (coord):
	return pg.Rect((coord[0]-(clawWidth/2), coord[1]-(clawHeight/2), clawWidth, clawHeight))

while not exitGame:
	for event in pg.event.get():
		if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
			exitGame = True
	
	screen.fill(background)
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (blurSize, blurSize), 0)
	
	# Saving the previous coordinates of the fingers (for smoother motion as well as collision related things)
	'''if thumbCoord != None:
		thumbPrev= thumbCoord
		indexPrev = indexCoord'''
	
	# Calling the function to find the coordinates of the trackers attached to the fingers
	thumbCoord = track.fingerTrack(hsv, thumb, frame)	
	if thumbCoord != None:
		indexCoord = track.fingerTrack(hsv, index, frame)
		if indexCoord == None:
			indexCoord = thumbCoord

	# We only want the index to move up and down above the thumb. It should always stay in line with the thumb
	if thumbCoord != None and indexCoord!=None:
		indexCoord = (thumbCoord[0], indexCoord[1])
		if indexCoord[1] > thumbCoord[1]:
			indexCoord = (indexCoord[0], thumbCoord[1]-clawHeight) 

	if thumbCoord != None:
		pg.draw.rect(screen, lowerClaw, coordToRect(thumbCoord))
		pg.draw.rect(screen, upperClaw, coordToRect(indexCoord))

	pg.display.flip()
	clock.tick(60)
