import tkinter as tk
from tkinter import ttk
from tkinter import *
import constants as constants

LARGE_FONT = ("Verdana", 35)

# consists of:
# a button to open a session
# a button to create a session
# a button to go to settings
class HomePage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = ttk.Label(self, text=constants.HOME, font=LARGE_FONT)
		label.place(relx=0.5, rely=0.2, anchor=CENTER)

		# Switch to NEW_SESSION
		new_session_btn = ttk.Button(self, text=constants.NEW_SESSION,
			command=lambda : controller.show_frame(NewSessionPage))
		new_session_btn.place(relx=0.75, rely=0.5, anchor=CENTER)

		# Switch to OPEN_SESSION
		open_session_btn = ttk.Button(self, text=constants.OPEN_SESSION,
			command=lambda : controller.open_session_popup(
			constants.EXAMPLE_SESSIONS, controller.handle_selected_item))
		open_session_btn.place(relx=0.25, rely=0.5, anchor=CENTER)

		# Switch to SETTINGS
		settings_btn = ttk.Button(self, text=constants.SETTINGS, 
			command= lambda: controller.show_frame(SettingsPage))
		settings_btn.place(relx=0.5, rely=0.8, anchor=CENTER)


class NewSessionPage(tk.Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		label = ttk.Label(self, text="HIIII", font=LARGE_FONT)
		label.place(relx=0.5, rely=0.5, anchor=CENTER)


# consists of:
# a sidebar with a list of sessions
# a list of settings that can be edited
# a button to save/update the settings
class SettingsPage(tk.Frame):
	
	def __init__(self, parent, controller):

		row = 0;
		
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text =constants.SETTINGS, font = LARGE_FONT)
		label.grid(row = row, column = 4, padx = 10, pady = 10)
		row+=1

		# Switch to HOME
		btn_home = ttk.Button(self, text =constants.HOME,
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = row, column = 1, padx = 10, pady = 10)
		row+=1

		# # Switch to SESSIONS
		# btn_session = ttk.Button(self, text =constants.SESSION,
		# 					command = lambda : controller.show_frame(SessionPage))
		# btn_session.grid(row = row, column = 1, padx = 10, pady = 10)
		# row+=1

		btn_test_popup = ttk.Button(self, text ="TEST",
							command = lambda : controller.open_popup("test message", True))
		btn_test_popup.grid(row = row, column = 1, padx = 10, pady = 10)
		row+=1


# consists of:
# a play/pause button
# a restart button
# a +5s button
# a show answer button
# an answer text label (hidden until answer button pressed)
# 2 success/fail buttons
class SessionPage(tk.Frame):

	def __init__(self, parent, controller, sessionName=constants.SESSION):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text =sessionName, font = LARGE_FONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# switch to HOME
		btn_home = ttk.Button(self, text =constants.HOME,
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = 1, column = 1, padx = 10, pady = 10)

		# switch to SETTINGS
		btn_sessions = ttk.Button(self, text =constants.SETTINGS,
							command = lambda : controller.show_frame(SettingsPage))
		btn_sessions.grid(row = 2, column = 1, padx = 10, pady = 10)


class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
		
		# Setup
		self.title(constants.APP_TITLE)
		self.geometry('350x200') #widthxheight
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (HomePage, NewSessionPage, SettingsPage, SessionPage):

			frame = F(container, self)

			# initializing frame of that object from startpage, page1, page2 respectively with for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(HomePage)

	# change pages
	def show_frame(self, cont, *args):
		frame = self.frames[cont]
		frame.tkraise(*args)

	# generic message popup helper
	def open_popup(self, message, isBlocking):
		popup = tk.Toplevel(self)
		popup.wm_title("Popup")
		popup.geometry('50x50')
		# popup.overrideredirect(True) # hide minimize/x button/drag bar

		# Calculate the center coordinates for the popup window
		app_x = self.winfo_x()
		app_y = self.winfo_y()
		app_width = self.winfo_width()
		app_height = self.winfo_height()
		popup_width = 200
		popup_height = 100
		x = app_x + app_width // 2 - popup_width // 2
		y = app_y + app_height // 2 - popup_height // 2

		popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")  # Set popup window size and position


		label = tk.Label(popup, text=message)
		label.pack(side="top", fill="x", pady=10)
		button = ttk.Button(popup, text="Close", command=popup.destroy)
		button.pack()
		if isBlocking:
			popup.grab_set()
			self.wait_window(popup)

	# popup for selecting a session
	def open_session_popup(self, items, callback):
		popup = tk.Toplevel(self)
		popup.wm_title("Select an Item")

		listbox = tk.Listbox(popup)
		for item in items:
			listbox.insert(tk.END, item)
		listbox.pack()

		# Calculate the center coordinates for the popup window
		app_x = self.winfo_x()
		app_y = self.winfo_y()
		app_width = self.winfo_width()
		app_height = self.winfo_height()
		popup_width = 200
		popup_height = 100
		x = app_x + app_width // 2 - popup_width // 2
		y = app_y + app_height // 2 - popup_height // 2

		popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")  # Set popup window size and position

		# Function to handle item selection
		def on_select():
			selected_index = listbox.curselection()
			if selected_index:
				selected_item = listbox.get(selected_index)
				callback(selected_item)
			popup.destroy()

		# Bind double-click event to the listbox
		listbox.bind("<Double-Button-1>", lambda event: on_select())

		# Okay button to confirm selection
		okay_button = ttk.Button(popup, text="Okay", command=lambda: on_select())
		okay_button.pack()

		# Make the popup modal (force user interaction)
		popup.grab_set()

		# Wait until the popup is closed before continuing
		self.wait_window(popup)


	# example callback for selecting a session
	def handle_selected_item(self, item):
		print(f"Selected item: {item}")
		self.show_frame(SessionPage)	


if __name__ == '__main__':
	app = tkinterApp()
	app.mainloop()
