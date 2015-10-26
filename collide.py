def inbounds(px, py, rect):
	x, y, width, height = rect
	return px > x and  px < x+width and py > y and py < y+width
	
# Detects collision by checking if any corner of one rect is inside the other rect
def detect(rect1, rect2):
	x, y, width, height = rect1
	return inbounds(x, y, rect2) or inbounds(x, y+height, rect2) or inbounds(x+width, y+height, rect2) or inbounds(x+width, y, rect2)

# This is the only function we use. It returns true if bottom of upper claw is touching/inside box AND top of lowerClaw is touching/inside box and the x coordinates also match	
def holding(box, upperClaw, lowerClaw):
	return \
	(box[1] - upperClaw[1] <= upperClaw[3]) and \
	(lowerClaw[1] - box[1] <= box[3]) and \
	((lowerClaw[0] > box[0] and lowerClaw[0] < box[0]+box[2]) or (lowerClaw[0]+lowerClaw[2] > box[0] and lowerClaw[0]+lowerClaw[2] < box[0]+box[2])) 

