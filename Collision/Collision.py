import math
import random

class CollisionDetector:

	def __init__(self, canvas):
		self.canvas = canvas

		# assign all the the relevant arrays for the bearing to angle loop
		self.exclusions = []
		self.sin = [1,-1,-1,1]
		self.cos = [1,1,-1,-1]
		self.bearings = [-1,1,-1,1]
		self.angles = [1,-1,1,-1]
		self.ifcompare = [math.pi*(1/2), math.pi, math.pi*(3/2), math.pi*2]
		self.realangles = [math.pi*(1/2), math.pi*(1/2), math.pi*(3/2), math.pi*(3/2)]

	# appends a shape exclusion to the array of exclusions
	def add_exclusion(self, exclusion):
		self.exclusions.append(exclusion)

	# handles the automated movement of a robot
	def ai_move(self, robot):

		# set the initial x and y movements in case they cannot be determined from the current bearing
		xmove = 0.0
		ymove = 0.0

		# from the current bearing, calculate the acute angle between the horizontal
		for i in range(0, len(self.sin)):
			if robot.bearing <= self.ifcompare[i]:
				angle = (self.angles[i]*self.realangles[i])+(robot.bearing*self.bearings[i])
				xmove = math.ceil(self.cos[i]*robot.velocity*math.cos(angle))
				ymove = math.ceil(self.sin[i]*robot.velocity*math.sin(angle))
				break

		# get the current positon of the robot and create a new coordinate set for the next movement
		coords = robot.center_position()
		points = (int(coords[0] + xmove), int(coords[1] + ymove), coords[0], coords[1])

		# determine whether we are working with a positive or negative x/y displacement
		if points[0] > points[2]:
			dx = points[0] - points[2]
			pvex = 1
		else:
			dx = points[2] - points[0]
			pvex = -1

		if points[1] > points[3]:
			dy = points[1] - points[3]
			pvey = 1
		else:
			dy = points[3] - points[1]
			pvey = -1

		# consideration needs to be made for the possibility of a 0 gradient and for a dx 0 due to the loop through the dx values
		if points[2]-points[0] is not 0:
			m = float(points[3]-points[1]) / float(points[2]-points[0])
		else:
			m = 0

		# two vars that hold the collision status and the current coordinates
		collision = False
		current_coords = None

		if dx > dy:
			# loop through the x movements
			for i in range(0, dx):
				# determine the x and y coords from the gradient of the line
				xcoord = pvex*i
				ycoord = math.ceil(m*xcoord)

				# get the coordinates of the next movement
				coords = (points[2]+xcoord-robot.half_width, points[3]+ycoord-robot.half_height, points[2]+xcoord+robot.half_width, points[3]+ycoord+robot.half_height)

				# check for collisions in the coordinate set
				overlapping = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])

				# if the coordinates are inside of the canvas, check if any of the shapes being collided with are within the exclusion list
				if coords[0] > 0 and coords[1] > 0 and coords[2] < self.canvas.width and coords[3] < self.canvas.height:
					for shape in overlapping:
						# if the shape does not equal the current robot and its not in the exclusions
						if not shape == robot.robot and self.exclusions.count(shape) == 0:
							collision = True
							break
				else:
					collision = True

				# if a collision has occured, break out of the loop
				if collision:
				    break

				# store the current coords
				current_coords = (coords[0], coords[1])
		else:
			for i in range(0, dy):
				# determine the x and y coords from the gradient of the line
				ycoord = pvey*i
				# check for zero gradient to ensure no division by zero happens
				if m == 0:
					xcoord = 0
				else:
					xcoord = math.ceil(ycoord/m)

				# get the coordinates of the next movement
				coords = (points[2]+xcoord-robot.half_width, points[3]+ycoord-robot.half_height, points[2]+xcoord+robot.half_width, points[3]+ycoord+robot.half_height)

				# check for collisions in the coordinate set
				overlapping = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
				
				# if the coordinates are inside of the canvas, check if any of the shapes being collided with are within the exclusion list
				if coords[0] > 0 and coords[1] > 0 and coords[2] < self.canvas.width and coords[3] < self.canvas.height:
					for shape in overlapping:
						if not shape == robot.robot and self.exclusions.count(shape) == 0:
							collision = True
							break
				else:
					collision = True

				# if a collision has occured, break out of the loop
				if collision:
					break

				# store the current coords
				current_coords = (coords[0], coords[1])

		# if there was a collision then switch the robot image to the collision state, otherwise move the robot to the coords
		if collision:
			if not robot.collision_status:
				robot.switch_image()
			
			# calculate a new bearing for the robot making sure it does not exceed 2pi and is no less than 0
			if (robot.bearing + math.pi/2) > math.pi*2:
				robot.bearing -= math.pi/2
			elif (robot.bearing - math.pi/2) < 0:
				robot.bearing += math.pi/2
			else:
				if random.randint(-1, 1) > 0:
					robot.bearing += math.pi/2
				else:
					robot.bearing -= math.pi/2
		else:
			if robot.collision_status:
				robot.switch_image()
			# if the robot has moved in a certain direction for intervals greater than the max movements, reset the counter and the bearing
			if robot.counter >= robot.max_movements:
				robot.reset_counter()

				# calculate a new bearing for the robot making sure it does not exceed 2pi and is no less than 0
				randomangle = random.uniform(math.pi/12, math.pi/6)
				if (randomangle + robot.bearing) > math.pi*2:
					robot.bearing -= randomangle
				elif (randomangle + robot.bearing) < 0:
					robot.bearing += randomangle
				else:
					if random.randint(-1, 1) > 0:
						robot.bearing += randomangle
					else:
						robot.bearing -= randomangle
			# move the robot to the new position
			self.canvas.coords(robot.robot, current_coords)
			robot.increment_counter()



	def find_collision(self, points, robot):

		# determine whether we are working with a positive or negative x/y displacement
		if points[0] > points[2]:
			dx = points[0] - points[2]
			pvex = 1
		else:
			dx = points[2] - points[0]
			pvex = -1

		if points[1] > points[3]:
			dy = points[1] - points[3]
			pvey = 1
		else:
			dy = points[3] - points[1]
			pvey = -1

		# consideration needs to be made for the possibility of a 0 gradient and for a dx 0 due to the loop through the dx values
		if points[2]-points[0] is not 0:
			m = float(points[3]-points[1]) / float(points[2]-points[0])
		else:
			m = 0
			return True
		test = 0

		# check to see which one of the x or y movements would produce the most accurate movement
		if dx > dy:
			# loop through the x movements
			for i in range(0, dx):
				# determine the x and y coords from the gradient of the line
				xcoord = pvex*i
				ycoord = math.ceil(m*xcoord)

				# get the coordinates of the next movement
				coords = (points[2]+xcoord-robot.half_width, points[3]+ycoord-robot.half_height, points[2]+xcoord+robot.half_width, points[3]+ycoord+robot.half_height)

				# check for collisions in the coordinate set
				overlapping = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])

				# if the coordinates are inside of the canvas, check if any of the shapes being collided with are within the exclusion list
				if coords[0] > 0 and coords[1] > 0 and coords[2] < self.canvas.width and coords[3] < self.canvas.height:
					for shape in overlapping:
						# if the shape does not equal the current robot
						if self.exclusions.count(shape) == 0:
							counter = 0
							for robot in self.canvas.robots:
								if shape == robot.robot:
									counter += 1
							if counter == 0:
								return True
				else:
					return True
		else:
			# loop through the y movements
			for i in range(0, dy):
				# determine the x and y coords from the gradient of the line
				ycoord = pvey*i
				# check for zero gradient to ensure no division by zero happens
				if m == 0:
					xcoord = 0
				else:
					xcoord = math.ceil(ycoord/m)

				# get the coordinates of the next movement
				coords = (points[2]+xcoord-robot.half_width, points[3]+ycoord-robot.half_height, points[2]+xcoord+robot.half_width, points[3]+ycoord+robot.half_height)

				# check for collisions in the coordinate set
				overlapping = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
				
				# if the coordinates are inside of the canvas, check if any of the shapes being collided with are within the exclusion list
				if coords[0] > 0 and coords[1] > 0 and coords[2] < self.canvas.width and coords[3] < self.canvas.height:
					for shape in overlapping:
						# if the shape does not equal the current robot
						if self.exclusions.count(shape) == 0:
							counter = 0
							for robot in self.canvas.robots:
								if shape == robot.robot:
									counter += 1
							if counter == 0:
								return True
				else:
					return True
		return False


	def move_route(self, robot):

		# if the route is not loaded do not continue execution of function
		if robot.route is None:
			return

		# calculate the new x and y movements and retrieve the previous and current node for later use
		xmove = robot.route.previous_point[0] + int(robot.velocity * math.cos(robot.route.angle))
		ymove = robot.route.previous_point[1] + int(robot.velocity * math.sin(robot.route.angle))
		node = robot.route.previous_node()
		current_node = robot.route.current_node()

		has_passed = False
		# if the next movement surpasses the node we are travelling to, set the x and y coords to the node
		if ((xmove + node[0]) > current_node[0] and robot.route.pvex > 0) or ((node[0] - xmove) < current_node[0] and robot.route.pvex < 0) or ((ymove + node[1]) > current_node[1] and robot.route.pvey > 0) or ((node[1] - ymove) < current_node[1] and robot.route.pvey < 0):
			xmove = current_node[0] - node[0]
			ymove = current_node[1] - node[1]
			has_passed = True

		# two vars that hold the collision status and the current coordinates
		collision = False
		current_coords = None

		# check to see which one of the x or y movements would produce the most accurate movement
		if xmove > ymove:
			# loop through the x movements
			for i in range(robot.route.previous_point[0], xmove):
				# determine the x and y coords from the gradient of the line
				xcoord = robot.route.pvex*i
				ycoord = math.ceil(robot.route.gradient*xcoord)

				# get the coordinates of the next movement
				coords = (node[0]+xcoord-robot.half_width, node[1]+ycoord-robot.half_height, node[0]+xcoord+robot.half_width, node[1]+ycoord+robot.half_height)

				# check for collisions in the coordinate set
				overlapping = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])

				# if the coordinates are inside of the canvas, check if any of the shapes being collided with are within the exclusion list
				if coords[0] > 0 and coords[1] > 0 and coords[2] < self.canvas.width and coords[3] < self.canvas.height:
					for shape in overlapping:
						if not shape == robot.robot and self.exclusions.count(shape) == 0:
							collision = True
							break
				else:
					collision = True

				# if a collision has occured, break out of the loop
				if collision:
					break

				# store the current coords
				current_coords = (coords[0], coords[1])

		else:
			# loop through the y movements
			for i in range(robot.route.previous_point[1], ymove):
				# determine the x and y coords from the gradient of the line
				ycoord = robot.route.pvey*i
				xcoord = math.ceil(ycoord/robot.route.gradient)

				# get the coordinates of the next movement
				coords = (node[0]+xcoord-robot.half_width, node[1]+ycoord-robot.half_height, node[0]+xcoord+robot.half_width, node[1]+ycoord+robot.half_height)

				# check for collisions in the coordinate set
				overlapping = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
				
				# if the coordinates are inside of the canvas, check if any of the shapes being collided with are within the exclusion list
				if coords[0] > 0 and coords[1] > 0 and coords[2] < self.canvas.width and coords[3] < self.canvas.height:
					for shape in overlapping:
						if not shape == robot.robot and self.exclusions.count(shape) == 0:
							collision = True
							break
				else:
					collision = True

				# if a collision has occured, break out of the loop
				if collision:
					break
				# store the current coords
				current_coords = (coords[0], coords[1])


		# if there was a collision then switch the robot image to the collision state, otherwise move the robot to the coords
		if collision:
			if not robot.collision_status:
				robot.switch_image()
		else:
			if robot.collision_status:
				robot.switch_image()
			self.canvas.coords(robot.robot, current_coords)
			robot.route.previous_point[0] = xmove
			robot.route.previous_point[1] = ymove


		# if the robot has surpassed the node it is travelling to then start processing the next node
		if has_passed:
			robot.route.currentnode += 1
			# if the current node is the last node of the route then remove the route to stop execution otherwise, continue calculation for the next node
			if robot.route.currentnode is len(robot.route.nodes):
				robot.route = None
			else:
				robot.route.calculate_route()