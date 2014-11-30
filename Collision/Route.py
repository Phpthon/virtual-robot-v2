import math

class Route:

	def __init__(self, nodes, robot):
		self.nodes = nodes
		self.robot = robot

		# assign relevant variables initial values
		self.currentnode = 1
		self.pvex = 1
		self.pvey = 1
		self.angle = 0.0
		self.gradient = 0.0
		self.previous_point = [0, 0]

	# returns the coordinates of the current node
	def current_node(self):
		return (self.nodes[self.currentnode][0], self.nodes[self.currentnode][1])

	# returns the coordinates of the current node
	def previous_node(self):
		return (self.nodes[self.currentnode-1][0], self.nodes[self.currentnode-1][1])

	# calculates the route information from one node to the next
	def calculate_route(self):
		
		# get the current and previous nodes
		next_node = self.current_node()
		previous_node = self.previous_node()

		# determine the angle incline/decline from the horizontal and whether we are travelling in a positive/negative x/y
		if next_node[1] > previous_node[1] and next_node[0] > previous_node[0]:
			opposite = next_node[1] - previous_node[1]
			adjacent = next_node[0] - previous_node[0]
			angle = math.atan2(opposite, adjacent)
			self.pvex = 1
			self.pvey = 1

		elif next_node[1] > previous_node[1] and next_node[0] < previous_node[0]:
			opposite = next_node[1] - previous_node[1]
			adjacent = previous_node[0] - next_node[0]
			angle = math.atan2(opposite, adjacent)
			self.pvex = -1
			self.pvey = 1

		elif next_node[1] < previous_node[1] and next_node[0] > previous_node[0]:
			opposite = previous_node[1] - next_node[1]
			adjacent = next_node[0] - previous_node[0]
			angle = math.atan2(opposite, adjacent)
			self.pvex = 1
			self.pvey = -1

		elif next_node[1] < previous_node[1] and next_node[0] < previous_node[0]:
			opposite = previous_node[1] - next_node[1]
			adjacent = previous_node[0] - next_node[0]
			angle = math.atan2(opposite, adjacent)
			self.pvex = -1
			self.pvey = -1

		# calculate the gradient of the path between the nodes and set the relevant path information
		self.gradient = (float(next_node[1]) - float(previous_node[1])) / float((next_node[0]) - float(previous_node[0]))
		self.angle = angle
		# reset the previous point
		self.previous_point = [0, 0]