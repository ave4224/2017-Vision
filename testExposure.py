import PiCamera, Printing

for i in range(1000,50000, 5000):
	print PiCamera.camera.exposure_speed, i
	image = PiCamera.getImage()
	PiCamera.set(shutter_speed=i)
	Printing.save(image)

