import math

# ONLY COMING FROM LEFT

robotLength = 2

def getXY():
	x,y = 1,1 # Get from Vision and LIDAR
	return x, y - robotLength


def getTheta():
	return math.pi / 2
	# Get from LIDAR
	# wall is horizontal
	# theta is radians robot is off of horizontal (straight forward is pi/2)
	# Range from -pi/2 to 3pi/2 (hopefully)

def circleArc(r, theta): #follows circle path until facing forward
	if no theta specified:
		turn until facing straight
	else:
		turn for theta / (radians per second) #seconds
	rightMotor, leftMotor = calculateMotorsTurn()
	both += speed # speed = (radians per second) * r

def forward(distance):
	rightMotor, leftMotor = defaultSpeed

def align():
	x, y = getXY()
	theta = getTheta()
	if theta > math.pi/2:
		turnRight(theta - math.pi/2)
	elif theta < 0:
		turnLeft(-theta)
	if y < x*math.cos(theta)/(1-math.sin(theta)): # y < r*cos(theta)
		turnRight() #solve for theta

	# while theta > math.pi/2:
	# 	turnRight()
	# 	theta = getTheta() # don't recalculate from lidar, but know how much robot turned from encoders?
	# while theta < 0:
	# 	turnLeft()
	# 	theta = getTheta() # don't recalculate from lidar, but know how much robot turned from encoders?
	# ratio = y/x # not recalculating because assuming that x,y are staying the same while turning
	# while ratio < math.cos(theta)/(1-math.sin(theta)): # y < r*cos(theta)
	# 	turnRight()
	# 	theta = getTheta()

	r = x/(math.sin(theta)-1)
	extraDist = y - r*cos(theta)
	circleArc(r, math.pi/2-theta)
	# Theta and x should be 0 now
	# y should equal extraDist (recalculate anyways)
	x, y = getXY()
	forward(y)


# Make y a little smaller for breathing room?
# Account for size and shape of robot?
# Make function iteratable (recalculate at every position to fix errors)
# Replace theta with math.pi/2 - theta
# Have speed limit variables and adjust speeds in different sections
#

def phi(d1, d2):
	d = 1/2 * sqrt(2*(d1^2+d2^2)-w^2)


# http://rossum.sourceforge.net/papers/CalculationsForRobotics/CubicPath.htm
# http://rossum.sourceforge.net/papers/CalculationsForRobotics/CirclePath.htm
# https://www.cs.bham.ac.uk/internal/courses/robotics/halloffame/2009/team8/path.html
