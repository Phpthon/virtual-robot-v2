# runs the program
from Main import Main
from Tkinter import *

# create  new instance of tk and pass the instance into the main program instance
root = Tk()
mainprogram = Main(root)

# execute the main loop which moves the robots
mainprogram.canvas.loop()

# execute the tkinter main loop
root.mainloop()