import cv2
camera = cv2.VideoCapture(0)

def getImage():
	retval, image = camera.read()
	return image

def set(resolution=False, exposure=False):
	if resolution:
		camera.set(3, resolution[0])
		camera.set(4, resolution[1])
	if exposure:
		camera.set(15, exposure)

def set(resolution=False, exposure=False):
	if resolution:
		return (camera.get(3), camera.get(4))
	if exposure:
		return camera.get(15)

def getExposure():
	return camera.get(15)
