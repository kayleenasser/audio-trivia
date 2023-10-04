import tkinter as tk
from tkinter import ttk
from tkinter import *
import constants as constants
import customtkinter as ctk
from CTkListbox import *
import trivia

LARGE_FONT = ('Verdana', 35)
MEDIUM_FONT = ('Verdana', 18)
SMALL_FONT = ('Verdana', 12)

# consists of:
# a button to open a session
# a button to create a session
# a button to go to settings
class HomePage(ctk.CTkFrame):

	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self, parent)

		label = ctk.CTkLabel(self, text=constants.HOME, font=LARGE_FONT)
		label.place(relx=0.5, rely=0.2, anchor=CENTER)

		# switch to CREATE_SESSION
		create_session_btn = ctk.CTkButton(self, text=constants.CREATE_SESSION,
			command=lambda : controller.show_frame(CreateSessionPage))
		create_session_btn.place(relx=0.75, rely=0.5, anchor=CENTER)

		# switch to OPEN_SESSION
		open_session_btn = ctk.CTkButton(self, text=constants.OPEN_SESSION,
			command=lambda : controller.open_session_popup(
			constants.EXAMPLE_SESSIONS, controller.handle_selected_session))
		open_session_btn.place(relx=0.25, rely=0.5, anchor=CENTER)

		# switch to SETTINGS
		settings_btn = ctk.CTkButton(self, text=constants.SETTINGS, 
			command= lambda: controller.show_frame(SettingsPage))
		settings_btn.place(relx=0.5, rely=0.8, anchor=CENTER)


class CreateSessionPage(ctk.CTkFrame):

	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self, parent)

		label = ctk.CTkLabel(self, text='Create a New Session', font=MEDIUM_FONT)
		label.place(relx=0.5, rely=0.1, anchor=CENTER)

		label = ctk.CTkLabel(self, text='Session Name', font=SMALL_FONT)
		label.place(relx=0.25, rely=0.2, anchor=CENTER)
		session_name = ctk.CTkEntry(self, width=15)
		session_name.place(relx=0.6, rely=0.2, anchor=CENTER)
		
		btn_home = ctk.CTkButton(self, text =constants.HOME,
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = 0, column = 0, padx = 10, pady = 10)
		


# consists of:
# a sidebar with a list of sessions
# a list of settings that can be edited
# a button to save/update the settings
class SettingsPage(ctk.CTkFrame):
	
	def __init__(self, parent, controller):

		row = 0
		
		ctk.CTkFrame.__init__(self, parent)
		label = ctk.CTkLabel(self, text =constants.SETTINGS, font = LARGE_FONT)
		label.grid(row = row, column = 4, padx = 10, pady = 10)
		row+=1

		# Switch to HOME
		btn_home = ctk.CTkButton(self, text =constants.HOME,
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = row, column = 1, padx = 10, pady = 10)
		row+=1

		# # Switch to SESSIONS
		# btn_session = ctk.Button(self, text =constants.SESSION,
		# 					command = lambda : controller.show_frame(SessionPage))
		# btn_session.grid(row = row, column = 1, padx = 10, pady = 10)
		# row+=1

		btn_test_popup = ctk.CTkButton(self, text ="TEST",
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
# a Retry button that picks a different timestamp from the same audio
class SessionPage(ctk.CTkFrame):

	def __init__(self, parent, controller, sessionName=constants.SESSION):
		ctk.CTkFrame.__init__(self, parent)

		row = 0
		self.lbl_title = ctk.CTkLabel(self, text =sessionName, font = LARGE_FONT)
		self.lbl_title.grid(row = row, column = 4, padx = 10, pady = 10)
		row+=1

		# NAV BUTTONS

		# switch to HOME
		btn_home = ctk.CTkButton(self, text =constants.HOME,
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = row, column = 1, padx = 10, pady = 5)
		row+=1

		# switch to SETTINGS
		btn_sessions = ctk.CTkButton(self, text =constants.SETTINGS,
							command = lambda : controller.show_frame(SettingsPage))
		btn_sessions.grid(row = row, column = 1, padx = 10, pady = 5)
		row+=1


		# AUDIO BUTTONS
		row = 1
		audio_button_column = 3
		
		# play/pause
		## get a symbol/icon eventually
		self.is_paused = True # default to paused (need to press play for first track)
		self.track_has_played = False # default, use this to prevent success/x button use until track played
		btn_play = ctk.CTkButton(self, text =constants.PLAY_BUTTON,
							command = lambda : self.toggle_state(
								[self.is_paused], 
								btn_play,
								constants.PLAY_BUTTON, 
								constants.PAUSE_BUTTON, 
								self.UpdatePlayToggle,
								self.trivia.PlayPauseTrack)
							)
		btn_play.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1

		# replay
		## get a symbol/icon eventually
		replay_button = ctk.CTkButton(self, text ="Relay",
							command = lambda : self.trivia.ReplayTrack())
		replay_button.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1


		# increase interval
		# lazy initialization, updates in the initialize_trivia()
		self.btn_increase = ctk.CTkButton(self, text="",
							command = lambda : self.trivia.IncreaseIntervalLength())
		self.btn_increase.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1

		# show/hide answer
		# toggle value when pressed and show/hide the answer label
		self.is_answer_showing = False
		btn_answer = ctk.CTkButton(self, text =constants.SHOW_ANSWER,
							command = lambda : self.toggle_state(
								[self.is_answer_showing], 
								btn_answer,
								constants.HIDE_ANSWER, 
								constants.SHOW_ANSWER, 
								self.UpdateAnswerToggle,
								self.ShowHideAnswer)
							)
		btn_answer.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1

		# this will change and can't be initialized once, so will have to move to a callback probably? We'll see 
		# self.answer = trivia.GetAnswer()
		self.lbl_answer = ctk.CTkLabel(self, text = "myanswer", font = SMALL_FONT)
		self.lbl_answer.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		self.lbl_answer.grid_remove()
		row+=1

		# success
		# add point (and go to next)
		btn_success = ctk.CTkButton(self, text ="Check",
							command = lambda : self.UpdateScore(is_success=True, callback=self.trivia.PlayNextTrack))
		btn_success.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1

		# failure
		# no points, just go to next
		btn_failure = ctk.CTkButton(self, text ="X",
							command = lambda : self.UpdateScore(is_success=False, callback=self.trivia.PlayNextTrack))
		btn_failure.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1

		# retry
		btn_retry = ctk.CTkButton(self, text ="Retry",
							command = lambda : self.trivia.ReplayTrack())
		btn_retry.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1

		# Score
		self.score_var = StringVar()
		self.score_var.set("Score: 0") # default
		self.lbl_score = ctk.CTkLabel(self, textvariable=self.score_var, font=SMALL_FONT)
		self.lbl_score.grid(row = 0, column = 0, padx = 5, pady = 5)
	
	# for play/pause and show/hide answer
	# need to make it a list so that it's mutable
	def toggle_state(self, state_list, button, true_text, false_text, updater, callback):
		state_list[0] = not state_list[0]
		# Toggle the state
		if state_list[0]:
			button.config(text=true_text)
		else:
			button.config(text=false_text)

		# Pass the current state to a function
		if updater:
			updater(state_list[0], callback)
	
	def UpdatePlayToggle(self, isPaused, callback):
		self.is_paused = isPaused
		# the first time (or rather, every time) it plays the track, update that one has been played. 
		# (this is to ensure we don't add score before it's been played)
		if not self.is_paused:
			self.track_has_played = True

		if callback:
			callback(self.is_paused)

	def UpdateAnswerToggle(self, is_answer_showing, callback):
		self.is_answer_showing = is_answer_showing
		if callback:
			callback(self.is_answer_showing)
	
	def UpdateScore(self, is_success, callback):
		if self.track_has_played:
			if is_success:
				self.trivia.UpdateScore()
				self.score_var.set(f"{self.trivia.GetScore()} points")
				app.update_idletasks() # update score immediately before continuing
		
			# typically play next song
			if callback:
				callback()

	
	def ShowHideAnswer(self, is_answer_showing):
		if is_answer_showing:
			self.answer = self.trivia.GetAnswer()
			self.lbl_answer.grid()
			self.lbl_answer.config(text=self.answer)
		else:
			self.lbl_answer.grid_remove()

	def initialize_trivia(self, session_name):
		# Check if trivia instance is already created
		if not (hasattr(self, 'trivia')):
			self.trivia = trivia.Trivia(session_name)  # Create Trivia instance here
		else:
			#reset when reopen sessionpage
			self.trivia.Reset(session_name)
		
		# reset/update buttons, labels, & score
		self.score_var.set(f"Score: {self.trivia.GetScore()}")
		self.btn_increase.config(text=f"+{self.trivia.GetIncreaseAmount()}s") # update the value once it's been initialized
		self.is_answer_showing = False
		self.track_has_played = False
		# force update
		app.update_idletasks()

class tkinterApp(ctk.CTk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):

		ctk.CTk.__init__(self, *args, **kwargs)
		ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
		ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
		# Setup
		self.title(constants.APP_TITLE)
		self.geometry('1000x1000') #widthxheight
		
		# creating a container
		container = ctk.CTkFrame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (HomePage, CreateSessionPage, SettingsPage, SessionPage):

			frame = F(container, self)

			# initializing frame of that object from startpage, page1, page2 respectively with for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(HomePage)
		
	

	# change pages
	def show_frame(self, cont, *args):
		frame = self.frames[cont]
		if cont == SessionPage:
			frame.initialize_trivia(self.session_name)  # Initialize Trivia instance before showing SessionPage
			frame.lbl_title.config(text=self.session_name)
		frame.tkraise(*args)

	# generic message popup helper
	def open_popup(self, message, isBlocking):
		popup = ctk.CTkToplevel(self)
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


		label = ctk.CTkLabel(popup, text=message)
		label.pack(side="top", fill="x", pady=10)
		button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
		button.pack()
		if isBlocking:
			popup.grab_set()
			self.wait_window(popup)

	# popup for selecting a session
	def open_session_popup(self, items, callback):
		popup = ctk.CTkToplevel(self)
		popup.wm_title("Select an Item")

		listbox = CTkListbox(popup)
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
		okay_button = ctk.CTkButton(popup, text="Okay", command=lambda: on_select())
		okay_button.pack()

		# Make the popup modal (force user interaction)
		popup.grab_set()

		# Wait until the popup is closed before continuing
		self.wait_window(popup)


	# example callback for selecting a session
	def handle_selected_session(self, session_name):
		self.session_name = session_name
		print(f"Selected item: {session_name}")
		self.show_frame(SessionPage)	

	

if __name__ == '__main__':
	app = tkinterApp()
	app.mainloop()
