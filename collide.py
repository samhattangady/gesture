def inbounds(px, py, rect):
	x, y, width, height = rect
	if px > x and  px < x+width and py > y and py < y+width:
		return True
	else:
		return False

def detect(rect1, rect2):
	x, y, width, height = rect1

	if inbounds(x, y, rect2) or inbounds(x, y+height, rect2) or inbounds(x+width, y+height, rect2) or inbounds(x+width, y, rect2):
		return True
	else:
		return False
