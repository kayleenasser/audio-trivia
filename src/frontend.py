import tkinter as tk
from tkinter import ttk
import constants as constants


LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
		
		# Setup
		self.title(constants.APP_TITLE)
		self.geometry('350x200') #widthxheight
		
		# MENU BAR
		menu = tk.Menu(self)
		item = tk.Menu(menu, tearoff=0)
		item.add_command(label=constants.SETTINGS)
		menu.add_cascade(label='File', menu=item)
		self.config(menu=menu)
		
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (HomePage, SettingsPage, SessionPage):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(HomePage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

class HomePage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = ttk.Label(self, text =constants.HOME, font = LARGEFONT)

		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# Switch to SETTINGS
		button1 = ttk.Button(self, text =constants.SETTINGS,
		command = lambda : controller.show_frame(SettingsPage))
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# Switch to SESSION
		button2 = ttk.Button(self, text =constants.SESSION,
		command = lambda : controller.show_frame(SessionPage))
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

class SettingsPage(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text =constants.SETTINGS, font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# Switch to LANDING PAGE
		button1 = ttk.Button(self, text =constants.HOME,
							command = lambda : controller.show_frame(HomePage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# Switch to SESSIONS
		button2 = ttk.Button(self, text =constants.SESSION,
							command = lambda : controller.show_frame(SessionPage))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)


class SessionPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text =constants.SESSION, font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# switch to HOME
		button1 = ttk.Button(self, text =constants.HOME,
							command = lambda : controller.show_frame(HomePage))
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# switch to SETTINGS
		button2 = ttk.Button(self, text =constants.SETTINGS,
							command = lambda : controller.show_frame(SettingsPage))
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)


# Driver Code
app = tkinterApp()
app.mainloop()
