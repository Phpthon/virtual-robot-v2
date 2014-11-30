# the main class does everything
import Tkinter as tk
import tkColorChooser
import tkFileDialog
from UI.Components import *
import threading
import time
from random import randrange
from FileIO import File
from Collision.Route import Route

class Main(tk.Frame):

	def __init__(self, master):

		tk.Frame.__init__(self, master)

		# set up the appopriate variables and look of the gui
		self.master.config(cursor="plus")
		master.config(background="white")
		self.master.title("Python Virtual Robot")
		self.selected_robot1 = True
		self.file = None
		self.current_node = None
		self.route = None

		# row/column weight configs

		self.master.grid_columnconfigure(0,weight=1)
		self.master.grid_columnconfigure(1, weight=0)
		self.master.grid_columnconfigure(2, weight=0)
		self.master.grid_columnconfigure(3, weight=0)
		self.master.grid_columnconfigure(4, weight=0)

		self.master.grid_rowconfigure(0,weight=0)
		self.master.grid_rowconfigure(1, weight=0)
		self.master.grid_rowconfigure(2,weight=0)
		self.master.grid_rowconfigure(3,weight=0)
		self.master.grid_rowconfigure(4,weight=1)
		self.master.grid_rowconfigure(5,weight=0)
		self.master.grid_rowconfigure(6,weight=0)
		self.master.grid_rowconfigure(7,weight=0)
		self.master.grid_rowconfigure(8,weight=0)
		self.master.grid_rowconfigure(9,weight=0)
		self.master.grid_rowconfigure(10,weight=1)
		self.master.grid_rowconfigure(11,weight=0)
		self.master.grid_rowconfigure(12,weight=0)
		self.master.grid_rowconfigure(13,weight=0)
		self.master.grid_rowconfigure(14,weight=0)

		# top left canvas

		self.canvas = Canvas(self.master, width=500, height=500, bg='white')
		self.canvas.grid(row=0, column=0, columnspan=2, rowspan=11, padx=5, pady=5)
		self.canvas.bind("<Button-1>", self.canvas_click)
		self.selected_robot = self.canvas.robot

		# title inbetween canvas and textarea

		title = Title(self.master, text="Console Log")
		title.grid(row=11, column=0, columnspan=2)
		
		# bottom textarea
		
		self.textarea = TextArea(self.master, width=5, height=5)
		self.scrollbar = tk.Scrollbar(self.master)
		self.scrollbar.config(command=self.textarea.yview)
		self.textarea.config(yscrollcommand=self.scrollbar.set)
		self.textarea.grid(row=12, column=0, rowspan=3, sticky="nesw", padx=(10, 0), pady=5)

		# textarea scrollbar

		self.scrollbar.grid(row=12, column=1, rowspan=3, sticky="nesw", pady=5, padx=(0, 10))

		# right top title

		title = Title(self.master, text="Route Information")
		title.grid(row=0, column=2, columnspan=3, padx=5, pady=5)

		# title for file and actual file name

		title = Title(self.master, text="File")
		title.grid(row=1, column=2, padx=5, pady=5)

		self.file_name = Label(self.master, text="")
		self.file_name.grid(row=1, column=3, columnspan=2, padx=5, pady=5)

		# 3 buttons for creating/saving/loading robocoord files

		button = Button(self.master, text="New", padx=5, pady=5)
		button.grid(row=2, column=2)
		button.bind("<Button-1>", self.new_file)

		button = Button(self.master, text="Save", padx=5, pady=5)
		button.grid(row=2, column=3)
		button.bind("<Button-1>", self.save_file)

		button = Button(self.master, text="Load", padx=5, pady=5)
		button.bind("<Button-1>", self.load_file)
		button.grid(row=2, column=4)

		# route nodes title

		title = Title(self.master, text="Route Nodes", padx=5, pady=5)
		title.grid(row=3, column=2, columnspan=3)

		# route nodes listbox

		self.node_list = Listbox(self.master)
		self.node_list.grid(row=4, column=2, columnspan=3, sticky="nesw", padx=5, pady=5)
		self.node_list.bind("<<ListboxSelect>>", self.node_select)

		self.textarea = TextArea(self.master, width=5, height=5)
		self.scrollbar = tk.Scrollbar(self.master)
		self.scrollbar.config(command=self.textarea.yview)
		self.textarea.config(yscrollcommand=self.scrollbar.set)
		self.textarea.add_line("Event", "File_Open", "The user opened an existing node list")
		self.textarea.add_line("Event", "Button_Click_1", "The user started the robot again")
		self.textarea.grid(row=12, column=0, rowspan=3, sticky="nesw", padx=(10, 0), pady=5)

		# textarea scrollbar

		self.scrollbar.grid(row=12, column=1, rowspan=3, sticky="nesw", pady=5, padx=(0, 10))

		# robot title and dropdown

		title = Title(self.master, text="Robot")
		title.grid(row=5, column=2, padx=5, pady=5)

		self.optionmenu = OptionMenu(self.master, ["Robot 1", "Robot 2"])
		self.optionmenu.grid(row=5, column=3, columnspan=2, sticky="nesw", padx=5, pady=5)
		self.optionmenu.selected_item.trace("w", self.change_robot)

		# robot settings

		title = Title(self.master, text="Robot Settings")
		title.grid(row=6, column=2, columnspan=3, padx=5, pady=5)

		title = Title(self.master, text="Velocity")
		title.grid(row=7, column=2, padx=5, pady=5)

		self.velocity = Scale(self.master, 5, 30, 10)
		self.velocity.grid(row=7, column=3, columnspan=2, sticky="nesw", padx=5, pady=5)
		self.velocity.bind("<ButtonRelease-1>", self.change_velocity)

		title = Title(self.master, text="Color")
		title.grid(row=9, column=2, padx=5, pady=5)

		self.colorbutton = tk.Button(self.master, borderwidth=0, bg="green")
		self.colorbutton.grid(row=9, column=3, columnspan=2, sticky="nesw", padx=5, pady=5)
		self.colorbutton.bind("<ButtonRelease-1>", self.robot_color)

		self.update_interface()

	# handles the velocity slider event
	def change_velocity(self, event):
		self.selected_robot.change_velocity(self.velocity.get())

	# handles the robot optionmenu event
	def change_robot(self, *args):
		# determine the robot that was selected by the user and update the gui accordingly
		if self.optionmenu.selected_item.get() == "Robot 1":
			self.selected_robot = self.canvas.robot
		else:
			self.selected_robot = self.canvas.robot1
		self.update_interface()

	# update the gui with the robot-specific properties
	def update_interface(self):
		self.velocity.set(self.selected_robot.velocity)
		self.colorbutton.config(bg=self.selected_robot.rgb_to_hex(self.selected_robot.previous_color))

	# handles the node list event
	def node_select(self, event):
		# if a node is selected
		if self.current_node is not None:
			# remove the circle on the selected node from the canvas
			self.canvas.collision_detector.exclusions.remove(self.current_node)
			self.canvas.delete(self.current_node)
			self.current_node = None
		# if the user selected a node
		if event is not None:
			widget = event.widget
			# check to see if the user actually selected a node or not
			if len(widget.curselection()) > 0:
				# draw a circle at the current node to alert the user of the position of the selected node
				index = int(widget.curselection()[0])
				coords = self.file.coords[index]
				halfsize = math.floor(10/2)
				self.current_node = self.canvas.create_oval(coords[0]-halfsize, coords[1]-halfsize, coords[0]+halfsize, coords[1]+halfsize, fill="#C0C0C0", width=0)
				self.canvas.tag_lower(self.current_node)
				self.canvas.collision_detector.exclusions.append(self.current_node)

	# adds a new node to the list of nodes
	def add_node(self, x, y):
		self.node_list.insert(tk.END, "[" + str(x) + ", " + str(y) + "]")

	# initialises the route for the robot to follow
	def init_route(self):
		# create a new route instance for the robot to follow and move the robot to the first node
		self.canvas.robots[1].route = Route(self.file.coords, self.canvas.robots[1])
		self.canvas.robots[1].route.calculate_route()
		self.canvas.coords(self.canvas.robots[1].robot, self.file.coords[0][0]-self.canvas.robots[1].half_width, self.file.coords[0][1]-self.canvas.robots[1].half_height)

	# handles the new button click event
	def new_file(self, event):
		# ask the user to create a .robocoord file
		f = tkFileDialog.asksaveasfile(parent=self.master, mode='a+', defaultextension=".robocoord", filetypes=(("Robot Coords", "*.robocoord"),))
		# set the file length to 0, removing any current nodes if the file already existed
		f.truncate(0)
		# if the user cancelled the dialog, stop execution of the function
		if f is None:
			return
		# send an empty event to remove any active node selection on the canvas
		self.node_select(None)
		# remove all of the nodes from the list of nodes
		self.node_list.delete(0, tk.END)
		# remove all of the lines between the nodes
		for line in self.canvas.path_lines:
			self.canvas.delete(line)
			self.canvas.collision_detector.exclusions.remove(line)

		# empty the path lines array and load the file
		self.canvas.path_lines = []
		self.file = File(f)
		self.file_name.config(text=self.file.file_name)

	# handles the save button click event
	def save_file(self, event):
		# if no file is open, stop execution of function
		if self.file is None:
			return
		# write any data in the buffer to the file and inform the user of the file being saved
		self.file.file.flush()
		self.textarea.add_line("File", "Saved", "The file " + self.file.file_name + " was saved successfully")

	# handles the load button click event
	def load_file(self, event):
		# ask the user to open a .robocoord file
		f = tkFileDialog.askopenfile(parent=self.master, mode='a+', defaultextension=".robocoord", filetypes=(("Robot Coords", "*.robocoord"),))
		# if the user cancelled the dialog, stop execution of function
		if f is None:
			return
		# send an empty event to remove any active node selection on the canvas
		self.node_select(None)
		# remove all of the nodes from the list of nodes
		self.node_list.delete(0, tk.END)
		# remove all of the lines between the nodes
		for line in self.canvas.path_lines:
			self.canvas.delete(line)
			self.canvas.collision_detector.exclusions.remove(line)

		# empty the path lines array and load the file
		self.canvas.path_lines = []
		self.file = File(f)
		self.file_name.config(text=self.file.file_name)

		# loop through all of the nodes and check if there are any collisions between them
		has_collision = False
		for i in range(1, len(self.file.coords)):

			has_collision = self.canvas.collision_detector.find_collision((self.file.coords[i][0], self.file.coords[i][1], self.file.coords[i-1][0], self.file.coords[i-1][1]), self.canvas.robot)
			if has_collision:
				self.textarea.add_line("File", "Error", "The file " + self.file.file_name + " contains an obstruction in the path")
				has_collision = True
				break

		# if there are no collisions between the nodes
		if not has_collision:
			# check to see if the file contains any nodes
			if len(self.file.coords) > 0:
				# add the node to the list of nodes
				self.add_node(self.file.coords[0][0], self.file.coords[0][1])
				# loop through the nodes and add the path lines between them
				for i in range(1, len(self.file.coords)):
					self.add_node(self.file.coords[i][0], self.file.coords[i][1])
					line = self.canvas.create_line(self.file.coords[i][0], self.file.coords[i][1], self.file.coords[i-1][0], self.file.coords[i-1][1], fill="#BDBDBD", dash=(4,4))
					self.canvas.path_lines.append(line)
					self.canvas.tag_lower(line)
					self.canvas.collision_detector.exclusions.append(line)
				self.textarea.add_line("File", "Success", "The path was successfully loaded from the file " + self.file.file_name)
				# initialise the route so the robot begins following it
				self.init_route()
			else:
				# the file contains no nodes and so the path is empty
				self.textarea.add_line("File", "Success", "The empty path was successfully loaded from the file " + self.file.file_name)

	def canvas_click(self, event):
		# if there is a coordinate set open
		if self.file is not None:
			# if there are coords in the file
			if len(self.file.coords) is not 0:
				# check for collisions between the new node and the previous node
				has_collision = self.canvas.collision_detector.find_collision((event.x, event.y, self.file.coords[len(self.file.coords)-1][0], self.file.coords[len(self.file.coords)-1][1]), self.canvas.robot)
				# if there was a collision, inform the user
				if has_collision:
					self.textarea.add_line("Error", "Collision", "The path between the chosen coords contains an obstruction")
				else:
					# there was no collision so add the new node to the file and create a line between the new and previous node. Also add the newly created lines to the shape exclusions
					self.file.write_coords(event.x, event.y)
					self.add_node(event.x, event.y)
					line = self.canvas.create_line(self.file.coords[len(self.file.coords)-1][0], self.file.coords[len(self.file.coords)-1][1], self.file.coords[len(self.file.coords)-2][0], self.file.coords[len(self.file.coords)-2][1], fill="#BDBDBD", dash=(4,4))
					self.canvas.path_lines.append(line)
					self.canvas.tag_lower(line)
					self.canvas.collision_detector.exclusions.append(line)
			else:
				# there are no coords in the file assume we are adding the first node and check for any collisions
				has_collision = self.canvas.collision_detector.find_collision((event.x, event.y, event.x-1, event.y-1), self.canvas.robot)
				if has_collision:
					self.textarea.add_line("Error", "Collision", "The chosen starting node is on an obstruction")
				else:
					self.file.write_coords(event.x, event.y)
					self.add_node(event.x, event.y)

	def robot_color(self, event):
		# get the users color selection
		(rgb, hx) = tkColorChooser.askcolor(parent=self, color=self.colorbutton.cget("bg"))
		# if the user has not cancelled the color selection
		if rgb is not None:
			# change the robot color accordingly
			self.selected_robot.change_color(rgb)
			self.colorbutton.config(bg=hx)
			self.textarea.add_line(self.optionmenu.selected_item.get(), "Color", "The robots color was changed to rgb " + str(rgb))