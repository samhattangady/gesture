# Final game file. We can pick up and move the box just by moving our fingers. Youll need good lighting and objects that do not clash with the background.

import pygame as pg
import numpy as np
import cv2
import colours as clr
import track
import collide
import calculations as calc

# Setting colours for fingers
thumb = clr.pinkHSV
index = clr.orangeHSV
background = clr.blueBeige
upperClaw = clr.blueBeige2
lowerClaw = clr.blueBeige3
boxColour = clr.red

clock = pg.time.Clock()

# Setting constants for game objects
claw= (45, 15)
blurSize = 5
speed = 1
thumbCoord= indexCoord= None # Initializing variables, because we need to store the past values.
box = (50, 50)
boxCoord = (160, 160)
border = 55 # Distance between bottom of screen and lowest position of box

# Starting camera, as well as finding the dimensions
cap = cv2.VideoCapture(0)
_, temp = cap.read()
resolution = temp.shape

pg.init()
screen = pg.display.set_mode((resolution[1], resolution[0])) # Resolution is actually storing number of rows and coloumns, so to convert that into x and y, we will need to reverse it.
exitGame = False

# Function to convert coordinates to pg.Rect
def coordToRect (coord, size):
	return pg.Rect((coord[0]-(size[0]/2), coord[1]-(size[1]/2), size[0], size[1]))

while not exitGame:
	for event in pg.event.get():
		if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
			exitGame = True
	
	screen.fill(background)
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (blurSize, blurSize), 0)
	fingerPresent = False
	
	# Calling the function to find the coordinates of the trackers attached to the fingers
	thumbCoord = track.fingerTrack(hsv, thumb, frame)	
	if thumbCoord != None:
		fingerPresent = True
		indexCoord = track.fingerTrack(hsv, index, frame)
		if indexCoord == None:
			indexCoord = thumbCoord

	if fingerPresent:
		holding = collide.holding(coordToRect(boxCoord,box), coordToRect(indexCoord, claw), coordToRect(thumbCoord,claw))
	
	# We only want the index to move up and down above the thumb. It should always stay in line with the thumb
	if fingerPresent:
		indexCoord = (thumbCoord[0], indexCoord[1])
		if indexCoord[1] > thumbCoord[1]:
			indexCoord = (indexCoord[0], thumbCoord[1]-claw[1]) 
	
	# Detecting collision between claw and box, and moving it with the claws when held. 
	if fingerPresent:
		if holding:
			boxCoord = (thumbCoord[0], (thumbCoord[1]+indexCoord[1])/2)	
			thumbCoord = (thumbCoord[0], boxCoord[1] + (box[1]/2) + (claw[1]/2))
			indexCoord = (thumbCoord[0], thumbCoord[1]-box[1]-claw[1])

	if boxCoord[1] >= resolution[0] - border:
		boxCoord = (boxCoord[0], resolution[0] - border)

	# Drawing the game objects
	pg.draw.rect(screen, boxColour, coordToRect(boxCoord, box))
	if fingerPresent:
		pg.draw.rect(screen, upperClaw, coordToRect(indexCoord, claw))
		pg.draw.rect(screen, lowerClaw, coordToRect(thumbCoord, claw))

	pg.display.flip()
	clock.tick(60)
