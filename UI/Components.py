import Tkinter as tk
from Collision.Collision import *
from Collision.Robot import *
import time
from datetime import datetime

# extends the tkinter Label class. for future style changes
class Label(tk.Label):

	def __init__(self, master, **options):
		options['font'] = ("Lucida Sans Unicode", 8, "normal")
		options['cursor'] = "center_ptr"
		options['background'] = "white"
		tk.Label.__init__(self, master, options)

# extends the tkinter Label class. for future style changes
class Title(tk.Label):

	def __init__(self, master, **options):
		options['font'] = ("Lucida Sans Unicode", 8, "bold")
		options['background'] = "white"
		tk.Label.__init__(self, master, options)

# extends the tkinter Button class. for future style changes
class Button(tk.Button):

	image_static = None
	image_hovered = None

	def __init__(self, master, **options):
		if Button.image_static is None:
			Button.image_static = tk.PhotoImage(file="Graphics/button.gif")
		if Button.image_hovered is None:
			Button.image_hovered = tk.PhotoImage(file="Graphics/button-hover.gif")

		options['image'] = Button.image_static
		options['borderwidth'] = 0
		options['compound'] = "center"
		options['background'] = "white"
		tk.Button.__init__(self, master, options)
		tk.Button.bind(self, "<Enter>", self.hover_state)
		tk.Button.bind(self, "<Leave>", self.leave_state)

	def hover_state(self, event):
		self.config(image=Button.image_hovered)

	def leave_state(self, event):
		self.config(image=Button.image_static)

# extends the tkinter Text class. for future style changes
class TextArea(tk.Text):

	def __init__(self, master, **options):
		tk.Text.__init__(self, master, options)
		options['font'] = ("Lucida Sans Unicode", 9, "normal")
		self.counter = 0

	def add_line(self, msgtype, title, text):
		self.counter += 1
		msgtype = "[" + msgtype + "]"
		title = "[" + title + "]: "
		self.insert("1.0", msgtype + title + text + "\n")
		self.tag_add("tag_" + str(self.counter), "1.0", "1." + str(len(msgtype + title)))
		self.tag_config("tag_" + str(self.counter), font=("Lucida Sans Unicode", 9, "bold"))

# extends the tkinter Listbox class. for future style changes
class Listbox(tk.Listbox):

	def __init__(self, master, **options):
		tk.Listbox.__init__(self, master, options)

# extends the tkinter OptionMenu class. for future style changes
class OptionMenu(tk.OptionMenu):

	def __init__(self, master, items):
		self.selected_item = tk.StringVar()
		self.selected_item.set(items[0])
		tk.OptionMenu.__init__(self, master, self.selected_item, *items)

# extends the tkinter Scale class. for future style changes
class Scale(tk.Scale):

	def __init__(self, master, from_, to, default):
		tk.Scale.__init__(self, master, orient=tk.HORIZONTAL, from_=from_, to=to)
		self.config(background="white")
		self.set(default)

# extends the tkinter Canvas class. for future style changes and used for holding the collision detector/robot instances
class Canvas(tk.Canvas):

	is_running = True

	def __init__(self, master, **kwargs):
		tk.Canvas.__init__(self, master, kwargs)

		self.master = master
		self.create_polygon([145,499,173,459,220,342,283,361,354,430,306,461,286,499])
		self.create_polygon([401,319,401,300,499,300,499,319])
		self.create_arc(400, -100, 500+100, 100, start=180, extent=90, fill="black")
		testing = self.create_polygon([225,200,250,90,330,90,360,190,290,260])
		poly = self.create_polygon([90,340,90,150,130,150,130,240,170,240,170,260,130,260,130,340])
		self.light = self.create_rectangle(0, 0, 25, 25, fill="green", width=0)


		self.robot = Robot(self, 30, 30, "robot-design.gif")
		self.robot1 = Robot(self, 300, 300, "robot-design.gif")
		self.robot1.change_color((255,152,31))

		self.robots = []
		self.robots.append(self.robot)
		self.robots.append(self.robot1)

		self.path_lines = []

		self.width = int(kwargs.get("width"))
		self.height = int(kwargs.get("height"))
		self.collision_detector = CollisionDetector(self)

		self.time = time.time()

	def add_shape_exclusion(self, shape):
		self.collision_detector.add_exclusion(shape)

	def toggle(self):
		if Canvas.is_running:
			self.itemconfig(self.light, fill="red")
			Canvas.is_running = False
		else:
			self.itemconfig(self.light, fill="green")
			Canvas.is_running = True

	# the main loop that is responsible for the movement of the robot
	def loop(self):

		# a more 'stable' approach of while True, infinite loop
		while 1:

			if (time.time() - self.time) > 5:
				self.toggle()
				self.time = time.time()
			if Canvas.is_running:
				self.collision_detector.ai_move(self.robots[0])
				self.collision_detector.move_route(self.robots[1])
			self.update()
			time.sleep(0.05)