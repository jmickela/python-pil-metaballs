#based on code found at: http://www.niksula.hut.fi/~hkankaan/Homepages/myprods/metaball.py.html
from math import sqrt
from PIL import Image, ImageDraw

BUFFER = 0
WIDTH = 256 + BUFFER*2
HEIGHT = 256 + BUFFER*2


class Ball:
	def __init__(self, x, y, size, group=0):
		self.pos = complex(x, y)
		self.x = x
		self.y = y
		self.size = size
		#if group is set the ball should only mesh with others in the same group
		self.group = group


class MetaBallManager:
	def __init__(self, balls, goo, threshold, color, image, image_size):
		self.balls = balls
		self.goo = goo
		self.threshold = threshold
		self.minSize = min([ball.size for ball in balls])
		self.image = image
		self.image_size = image_size
		self.color = color

	def DrawBalls(self, differentialMethod, step):
		# First, track the border for all balls and store
		# it to pos0 and edgePos. The latter will move along the border,
		# pos0 stays at the initial coordinates.
		for ball in self.balls:
			ball.pos0 = self.trackTheBorder(ball.pos + 1j)
			if ball.pos0 == None:
				ball.tracking = False
			else:
				ball.edgePos = ball.pos0
				ball.tracking = True
		# print "Done with tracking"

		loopIndex = 0
		while loopIndex < 200:
			loopIndex += 1
			for ball in self.balls:
				if not ball.tracking:
					continue

		 		# store the old coordinates
				old_pos = ball.edgePos

		 		# walk along the tangent, using chosen differential method
				ball.edgePos = differentialMethod(ball.edgePos, step, self.calcTangent)

		 		# correction step towards the border
				ball.edgePos, tmp = self.stepOnceTowardsBorder(ball.edgePos)

				draw = ImageDraw.Draw(self.image)
				draw.line((old_pos.real, old_pos.imag, ball.edgePos.real, ball.edgePos.imag), fill=self.color)
				del draw 

		 		# check if we've gone a full circle or hit some other
		 		# edge tracker
				for ob in self.balls:
					if ob.tracking:
						if (ob is not ball ) and abs(ob.pos0 - ball.edgePos) < step: #or loopIndex > 3
							ball.tracking = False

			tracking = 0
			for ball in self.balls:
				if ball.tracking:
					tracking += 1
				if tracking == 0:
					break
		for ball in self.balls:
			if ball.tracking:
				ball.pos = complex(round(ball.pos.real), round(ball.pos.imag))
				ImageDraw.floodfill(self.image, (ball.pos.real, ball.pos.imag), self.color) #, self.color)


	def calcForce(self, pos):
		#print 'in clacFOrce'
		"""Return the metaball field's force at point 'pos'."""
		force = 0
		for ball in self.balls:
			### Formula (1)
			div = abs(ball.pos - pos)**self.goo
			if div != 0: # to prevent division by zero
				force += ball.size / div
			else:
				force += 10000 #"big number"
		return force

	def calcNormal(self, pos):
		#print 'in calcNormal'
		"""Return a normalized (magnitude = 1) normal at point 'pos'."""
		np = 0j
		for ball in self.balls:
			### Formula (3)
			div = abs(ball.pos - pos)**(2 + self.goo)
			np += -self.goo * ball.size * (ball.pos - pos) / div
		return np / abs(np)

	def calcTangent(self, pos):
		#print 'in calcTangent'
		"""Return a normalized (magnitude = 1) tangent at point 'pos'."""
		np = self.calcNormal(pos)
		### Formula (7)
		return complex(-np.imag, np.real)

	def stepOnceTowardsBorder(self, pos):
		#print "in stepOnceTowardsBorder"
		"""Step once towards the border of the metaball field, return
		new coordinates and force at old coordinates.
		"""
		force = self.calcForce(pos)
		np = self.calcNormal(pos)

		### Formula (5)
		stepsize = (self.minSize / self.threshold)**(1 / self.goo) - (self.minSize / force)**(1 / self.goo) + 0.01
		return (pos + np * stepsize, force)

	def trackTheBorder(self, pos):
		#print "in trackTheBorder"
		"""Track the border of the metaball field and return new
		coordinates.
		"""
		force = 9999999
		# loop until force is weaker than the desired threshold
		while force > self.threshold:
			old_force = force
			pos, force = self.stepOnceTowardsBorder(pos)
			if abs(old_force - force) < 0.0000000001 or old_force < force:
				return None
		return pos

	def euler(self, pos, h, func):
		"""	Euler's method.
			The most simple way to solve differential systems numerically.
		"""
		return pos + h * func(pos)
	def rungeKutta2(self, pos, h, func):
		"""Runge-Kutta 2 (=mid-point).
		This is only a little more complex than the Euler's method,
		but significantly better.
		"""
		return pos + h * func(pos + func(pos) * h / 2)


	def plot_slow(self):
		#19 with numpy
		#6.9 seconds with member vars and calling plot_slow for each color

		#only used for comparison, too slow for most live site uses.
		pix = self.image.load()

		for x in range(0, WIDTH):
			for y in range(0, WIDTH):
				total = 0
				for ball in self.balls:
					#denominator = sqrt((ball.pos.item(0) - x)**2 + (ball.pos.item(1) - y)**2)**self.goo
					denominator = sqrt((ball.x - x)**2 + (ball.y - y)**2)**self.goo
					if denominator == 0:
						total += 10000
					else:
						total += ball.size / denominator
				if total > self.threshold:
					pix[x,y] = self.color
