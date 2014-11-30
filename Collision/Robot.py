import Tkinter as tk
import math

class Robot:

	def __init__(self, canvas, x, y, image_initial):
		self.canvas = canvas

		# set up all of the relevant variables and properties associated to the robot

		self.route = None

		self.image_initial = tk.PhotoImage(file="Graphics/" + image_initial)
		self.image_collision = tk.PhotoImage(file="Graphics/" + image_initial)

		self.robot = self.canvas.create_image(x, y, image=self.image_initial, anchor=tk.NW)

		self.half_width = math.ceil(self.width()/2)
		self.half_height = math.ceil(self.height()/2)

		self.velocity = 5
		self.bearing = 0.0
		self.counter = 0
		self.max_movements = 5

		self.collision_status = False
		self.current_colors = ["152 233 80", "134 197 77"]
		self.previous_color = None

		self.change_image_color((255, 0, 0), self.image_collision)
		self.change_color((152, 233, 80))

	# get the coords of the box surrounding the robot
	def coords(self):
		coords = self.canvas.coords(self.robot)
		coords.append(coords[0] + self.image_initial.width())
		coords.append(coords[1] + self.image_initial.height())
		return coords

	# get the center position of the robot
	def center_position(self):
		coords = self.canvas.coords(self.robot)
		return (int(coords[0] + math.floor(self.image_initial.width() / 2)), int(coords[1] + math.floor(self.image_initial.height() / 2)))

	# get the width of the robot
	def width(self):
		return self.image_initial.width()

	# get the height of the robot
	def height(self):
		return self.image_initial.height()

	# change the velocity of the robot
	def change_velocity(self, velocity):
		self.velocity = velocity

	# change the bearing that the robot sits on
	def change_bearing(self, bearing):
		self.bearing = bearing

	# change the max amount of movements before a new bearing is generated
	def change_max_movements(self, max_movements):
		self.max_movements = max_movements

	# reset the number of movements counter
	def reset_counter(self):
		self.counter = 0

	# increment the number of movements counter
	def increment_counter(self):
		self.counter += 1

	# changes the robots image if a collision happens
	def switch_image(self):
		# if the robot has collided
		if self.collision_status:
			# change the robots image back to its non-collision state
			self.collision_status = False
			self.canvas.itemconfig(self.robot, image=self.image_initial)			
		else:
			# change the robots image to its collision state
			self.collision_status = True
			self.canvas.itemconfig(self.robot, image=self.image_collision)

	# get hex equivalent of an rgb color
	def rgb_to_hex(self, rgb):
		return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

	# changes the color of the non-collision
	def change_image_color(self, newcolor, image):
		# get a darker shade of the new color
		darkcolor = [int(math.floor(newcolor[0]*0.75)), int(math.floor(newcolor[1]*0.75)), int(math.floor(newcolor[2]*0.75))]

		# get the hex values of the new rgb colors
		hexnew = self.rgb_to_hex(newcolor)
		hexdark = self.rgb_to_hex(darkcolor)
		# loop through each pixel of the robot image and change its color accordingly
		for i in range(image.width()):
			for j in range(image.height()):
				if str(image.get(i, j)) == self.current_colors[0]:
					image.put(hexnew, to=(i, j))
				elif str(image.get(i, j)) == self.current_colors[1]:
					image.put(hexdark, to=(i, j))

		# if the robot is not in its collision state, set the previous colors
		if image is self.image_initial:
			self.current_colors[0] = str(newcolor[0]) + " " + str(newcolor[1]) + " " + str(newcolor[2])
			self.current_colors[1] = str(darkcolor[0]) + " " + str(darkcolor[1]) + " " + str(darkcolor[2])

	# changes the color of the robot
	def change_color(self, newcolor):
		# changes the current robots color
		self.change_image_color(newcolor, self.image_initial)
		# changes the actual image on canvas
		self.canvas.itemconfig(self.robot, image=self.image_initial)
		# if the robot has not collided set the previous color to the current color
		if not self.collision_status:
			self.previous_color = newcolor