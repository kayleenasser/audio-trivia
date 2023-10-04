import json
import tkinter as tk
from tkinter import ttk
from tkinter import *
from sessions import _update_sessions_json
import util

import CTkListbox

import constants as constants
import customtkinter as ctk
from CTkListbox import *
import trivia
import sessions
import os
from PIL import Image, ImageTk

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
		self.controller = controller

		label = ctk.CTkLabel(self, text=constants.HOME, font=LARGE_FONT)
		label.place(relx=0.5, rely=0.35, anchor=N)

		label = ctk.CTkLabel(self, text=constants.WELCOME_TEXT, font=MEDIUM_FONT)
		label.place(relx=0.5, rely=0.5, anchor=CENTER)

		# switch to CREATE_SESSION
		create_session_btn = ctk.CTkButton(self, text=constants.CREATE_SESSION,
			command=lambda : controller.show_frame(CreateSessionPage),height= 50, width=250)
		create_session_btn.place(relx=0.45, rely=0.6, anchor=E)

		# switch to OPEN_SESSION
		open_session_btn = ctk.CTkButton(self, text=constants.OPEN_SESSION,
			command=lambda : self.OnOpenSessionClicked(),height= 50, width=250)
		open_session_btn.place(relx=0.55, rely=0.6, anchor=W)

		# switch to SETTINGS
		settings_btn = ctk.CTkButton(self, text=constants.SETTINGS, 
			command= lambda: controller.show_frame(SettingsPage),height= 10, width=10)
		settings_btn.place(relx=0.05, rely=0.95, anchor=SW)
		settings_btn.lift()
	
	def OnOpenSessionClicked(self):
		if sessions.get_num_sessions() == 1:
			# if only the default, we can't open any sessions so just go to create
			self.controller.show_frame(CreateSessionPage)
		else: 
			self.controller.open_session_popup(sessions.get_all_sessions(False))
			


class CreateSessionPage(ctk.CTkFrame):

	def __init__(self, parent, controller):
		ctk.CTkFrame.__init__(self, parent)

		label = ctk.CTkLabel(self, text='Create a New Session', font=LARGE_FONT)
		label.place(relx=0.5, rely=0.25, anchor=CENTER)

		label = ctk.CTkLabel(self, text='Please enter session name:', font=MEDIUM_FONT)
		label.place(relx=0.5, rely=0.4, anchor=CENTER)
		session_name = ctk.CTkEntry(self, width=200)
		session_name.place(relx=0.5, rely=0.5, anchor=CENTER)
		
		btn_home = ctk.CTkButton(self, text ="Back",
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = 0, column = 0, padx = 10, pady = 10)

		btn_OK = ctk.CTkButton(self, text = "OK",
							command = lambda : controller.show_frame(CreateSessionPage))
		btn_OK.place(relx=0.5, rely=0.6, anchor=CENTER)
		


# consists of:
# a sidebar with a list of sessions
# a list of settings that can be edited
# a button to save/update the settings
class SettingsPage(ctk.CTkFrame):
	
	def __init__(self, parent, controller):

		#initialize
		self.session_track_answers = [] 
		self.session_track_paths = []
		session_data = None
		row = 0
		
		ctk.CTkFrame.__init__(self, parent)
		# title label
		label = ctk.CTkLabel(self, text =constants.SETTINGS, font = LARGE_FONT)
		label.grid(row = row, column = 4, padx = 10, pady = 10)
		row+=1

		# Switch to HOME
		btn_home = ctk.CTkButton(self, text =constants.HOME,
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = row, column = 1, padx = 10, pady = 10)
		row+=1

		# get the sessions from the json
		# load them into the listbox
		self.UpdateSessionsList()
		self.listbox_sessions = CTkListbox(height=300, width=150, master=self, command=self.LoadAnswers)
		self.listbox_sessions.place(x=200, y=200)
		for i in range(0, len(self.sessions_list)):
			self.listbox_sessions.insert(i, self.sessions_list[i])

		# Other buttons
		btn_remove_session = ctk.CTkButton(self, text="Remove Session",
								 command=lambda: self.RemoveSession())
		btn_remove_session.place(x=50,y=300)

		btn_rename_session = ctk.CTkButton(self, text="Rename Session",
								 command=lambda: self.RenameSession())
		btn_rename_session.place(x=50,y=350)

		btn_create_session = ctk.CTkButton(self, text=constants.CREATE_SESSION,
								 command=lambda: controller.show_frame(CreateSessionPage))
		btn_create_session.place(x=50,y=400)


		#Songs Box
		self.listbox_tracks = CTkListbox(height=300, width=200, master=self,command=self.SelectTrackCallback)
		self.listbox_tracks.place(x=400, y=200)

		#Song option buttons
		btn_remove_song = ctk.CTkButton(self, text="Remove Song",
										   command=lambda: self.RemoveSong())
		btn_remove_song.place(x=630, y=280)

		btn_rename_song = ctk.CTkButton(self, text="Rename Song",
										   command=lambda: controller.show_frame(HomePage))
		btn_rename_song.place(x=630, y=330)

		btn_add_song = ctk.CTkButton(self, text="Add Song",
										command=lambda: controller.show_frame(HomePage))
		btn_add_song.place(x=630, y=480)

		# btn_test_popup = ctk.CTkButton(self, text ="TEST",
		# 					command = lambda : controller.open_popup("test message", True))
		# btn_test_popup.grid(row = row, column = 1, padx = 10, pady = 10)
		# row+=1

	def SelectTrackCallback(self, event):
		if event != None:
			print("selectrackcallback: ", event)
			self.selected_track = event

	def LoadAnswers(self, event):
		print("listbox event: ", event)
		if event is None:
			return
		# all the track answers for the session
		self.selected_session = event
		session_data = sessions.get_session(event)
		self.session_track_answers = []
		util.extract_data_from_json(session_data,
											constants.ANSWER_KEY,
											values=self.session_track_answers)
		# display them in the listbox
		for i in range(0,len(self.session_track_answers)):
			self.listbox_tracks.insert(i, self.session_track_answers[i])

	#remove and rename session button
	def RenameSession(self):
		print("RenameSession")
		selected_session_name = self.listbox_sessions.get(self.listbox_sessions.curselection())
		if not selected_session_name:
			return

		popup = ctk.CTkToplevel(self)
		popup.wm_title("Rename")
		popup.geometry('300x150')  # Set the size of the popup window

		txtbox_new_name = ctk.CTkEntry(popup, width=150)
		txtbox_new_name.pack(pady=10)
		txtbox_new_name.bind('<Return>', lambda event=None: ChangeSessionName())

		error_message = ctk.CTkLabel(popup, text="", text_color="red")
		error_message.pack()

		def ChangeSessionName():
			new_name = txtbox_new_name.get()
			if new_name in self.sessions_list:
				if new_name == constants.DEFAULT_SESSION:
					error_message.configure(text="Sorry, you can't choose this name.")
				else:
					error_message.configure(text="This session name already exists!")
			else:
				old_name = selected_session_name
				sessions.update_session_name(old_name, new_name)
				self.ReloadSessionListbox()
				popup.destroy()

		submit_btn = ctk.CTkButton(popup, text="Submit", command=ChangeSessionName)
		submit_btn.pack()

		# Center the popup window on the screen
		popup.update_idletasks()
		width = popup.winfo_width()
		height = popup.winfo_height()
		x = (popup.winfo_screenwidth() // 2) - (width // 2)
		y = (popup.winfo_screenheight() // 2) - (height // 2)
		popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))

		# Grab focus for the input field
		txtbox_new_name.focus_set()

		popup.grab_set()
		self.wait_window(popup)
	
	def RemoveSession(self):
		selected_session_name = self.listbox_sessions.get(self.listbox_sessions.curselection())
		if not selected_session_name:
			return
		sessions.delete_session(session_name=selected_session_name)
		self.ReloadSessionListbox()
	
	# with the assumption that we're dumping them in the box in order that they appear in the json
	# just going to get the path based on the index
	def RemoveSong(self):
		print("RemoveSong")
		self.session_track_paths = []
		util.extract_data_from_json(sessions.get_session(self.selected_session),
										constants.PATH_KEY,
										values=self.session_track_paths)
		print(self.listbox_tracks.curselection())
		track_to_remove = self.session_track_paths[self.listbox_tracks.curselection()]
		print("tracktoremove: ", track_to_remove)
		if not track_to_remove:
			return
		
		sessions.delete_audio_file(self.selected_session,track_to_remove)
		self.ReloadTrackListbox()

	def UpdateSessionsList(self):
		# exclude the default from the list
		self.sessions_list = list(sessions.get_all_sessions(False).keys())
		print(self.sessions_list)

	def UpdateTrackList(self):
		print("UpdateTrackList")
		# exclude the default from the list
		self.session_track_answers = []
		util.extract_data_from_json(sessions.get_session(self.selected_session),
											constants.ANSWER_KEY,
											values=self.session_track_answers)

	def ReloadSessionListbox(self):
			self.listbox_sessions.delete(0, tk.END)
			self.UpdateSessionsList()
			for i in range(0, len(self.sessions_list)):
				self.listbox_sessions.insert(i, self.sessions_list[i])
	
	def ReloadTrackListbox(self):
			print("ReloadTrackList")
			self.UpdateTrackList()
			self.listbox_tracks.delete(0, tk.END)
			print(self.session_track_answers)
			for i in range(0, len(self.session_track_answers)):
				self.listbox_tracks.insert(i, self.session_track_answers[i])



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
		self.lbl_title = ctk.CTkLabel(self, text=sessionName, font=LARGE_FONT)
		self.lbl_title.grid(row=row, column=4, padx=10, pady=10)
		row += 1

		# NAV BUTTONS

		# switch to HOME
		btn_home = ctk.CTkButton(self, text=constants.HOME,
			command=lambda : controller.show_frame(HomePage))
		btn_home.grid(row = row, column = 1, padx = 10, pady = 5)
		row += 1

		# switch to SETTINGS
		btn_sessions = ctk.CTkButton(self, text=constants.SETTINGS,
			command=lambda : controller.show_frame(SettingsPage))
		btn_sessions.grid(row=row, column=1, padx=10, pady=5)
		row += 1

		# AUDIO BUTTONS
		row = 1
		audio_button_column = 3
		
		# play/pause
		## get a symbol/icon eventually
		self.is_paused = True # default to paused (need to press play for first track)
		self.track_has_played = False # default, use this to prevent success/x button use until track played
		btn_play = ctk.CTkButton(self, text =constants.PLAY_BUTTON,
			command=lambda : self.toggle_state(
			[self.is_paused], btn_play, constants.PLAY_BUTTON,
			constants.PAUSE_BUTTON, self.UpdatePlayToggle,
			self.trivia.PlayPauseTrack))
		btn_play.grid(row=row, column=audio_button_column, padx=10, pady=5)
		row += 1

		# replay
		## get a symbol/icon eventually
		replay_button = ctk.CTkButton(self, text=constants.REPLAY_BUTTON,
			command=lambda : self.trivia.ReplayTrack())
		replay_button.grid(row=row, column=audio_button_column, padx=10, pady=5)
		row += 1


		# increase interval
		# lazy initialization, updates in the initialize_trivia()
		self.btn_increase = ctk.CTkButton(self, text="",
			command=lambda : self.trivia.IncreaseIntervalLength())
		self.btn_increase.grid(row=row, column=audio_button_column, padx=10, pady=5)
		row += 1

		# show/hide answer
		# toggle value when pressed and show/hide the answer label
		self.is_answer_showing = False
		btn_answer = ctk.CTkButton(self, text=constants.SHOW_ANSWER,
			command=lambda : self.toggle_state(
			[self.is_answer_showing], btn_answer, constants.HIDE_ANSWER,
			constants.SHOW_ANSWER, self.UpdateAnswerToggle,
			self.ShowHideAnswer))
		btn_answer.grid(row=row, column=audio_button_column, padx=10, pady=5)
		row += 1

		# this will change and can't be initialized once, so will have to move to a callback probably? We'll see 
		# self.answer = trivia.GetAnswer()
		self.lbl_answer = ctk.CTkLabel(self, text="myanswer", font=SMALL_FONT)
		self.lbl_answer.grid(row=row, column=audio_button_column, padx=10, pady=5)
		self.lbl_answer.grid_remove()
		row += 1

		# success
		# add point (and go to next)
		btn_success = ctk.CTkButton(self, text=constants.SUCCESS_BUTTON,
			command=lambda : self.UpdateScore(is_success=True, callback=self.trivia.PlayNextTrack))
		btn_success.grid(row=row, column=audio_button_column, padx=10, pady=5)
		row += 1

		# failure
		# no points, just go to next
		btn_failure = ctk.CTkButton(self, text=constants.FAILURE_BUTTON,
			command=lambda : self.UpdateScore(is_success=False, callback=self.trivia.PlayNextTrack))
		btn_failure.grid(row=row, column=audio_button_column, padx=10, pady=5)
		row += 1

		# retry
		btn_retry = ctk.CTkButton(self, text=constants.RETRY_BUTTON,
			command=lambda : self.trivia.PlayDifferentInterval())
		btn_retry.grid(row=row, column=audio_button_column, padx=10, pady=5)
		row += 1

		# Score
		self.score_var = StringVar()
		self.score_var.set("Score: 0") # default
		self.lbl_score = ctk.CTkLabel(self, textvariable=self.score_var, font=SMALL_FONT)
		self.lbl_score.grid(row=0, column=0, padx=5, pady=5)
	
	# for play/pause and show/hide answer
	# need to make it a list so that it's mutable
	def toggle_state(self, state_list, button, true_text, false_text, updater, callback):
		state_list[0] = not state_list[0]
		# Toggle the state
		if state_list[0]:
			button.configure(text=true_text)
		else:
			button.configure(text=false_text)

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
			self.lbl_answer.configure(text=self.answer)
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
		self.btn_increase.configure(text=f"+{self.trivia.GetIncreaseAmount()}s") # update the value once it's been initialized
		self.is_answer_showing = False
		self.track_has_played = False
		# force update
		app.update_idletasks()

class tkinterApp(ctk.CTk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):

		ctk.CTk.__init__(self, *args, **kwargs)
		ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
		ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
		self.after(201, lambda :self.iconbitmap('src\\assets\icon.ico'))
		# Setup
		self.title(constants.APP_TITLE)
		self.geometry('800x600') #widthxheight

		self.after(201, lambda :app.iconbitmap('src\\assets\icon.ico'))

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

		if cont == HomePage:
			self.initialize_banner()
		else:
			self.hide_banner()

		if cont == SessionPage:
			frame.initialize_trivia(self.session_name)  # Initialize Trivia instance before showing SessionPage
			frame.lbl_title.configure(text=self.session_name)
		frame.tkraise(*args)

	# generic message popup helper
	def open_popup(self, message, isBlocking):
		popup = ctk.CTkToplevel(self)
		popup.wm_title("Popup")
		popup.geometry('100x100')
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
	def open_session_popup(self, items):
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
			if selected_index is not None:
				selected_item = listbox.get(selected_index)
				self.session_name = selected_item
				self.show_frame(SessionPage)
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

	def initialize_banner(self):
		banner = Image.open("src\\assets\\dark-bg.PNG")
		banner_photo = ImageTk.PhotoImage(banner)
		self.banner_label = tk.Label(image=banner_photo)
		self.banner_label.configure(borderwidth=0)
		self.banner_label.image = banner_photo
		self.banner_label.place(relx=0.5, rely=0, anchor=N)

	def hide_banner(self):
		self.banner_label.place_forget()

	

if __name__ == '__main__':
	app = tkinterApp()
	app.mainloop()
