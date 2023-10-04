import json
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from sessions import _update_sessions_json

import CTkListbox

import constants as constants
import customtkinter as ctk
from CTkListbox import *
import trivia
import sessions
import os
from PIL import Image, ImageTk
from sessions import *
import os

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
		# banner = Image.open("src\\assets\\dark-bg.PNG")
		# banner_photo = ImageTk.PhotoImage(banner)
		# baner_label = tk.Label(image=banner_photo)
		# baner_label.config(borderwidth=0)
		# baner_label.image = banner_photo
		# # Position banner
		# baner_label.place(relx=0.5, rely=0, anchor=N)
		# baner_label

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

		audio = []

		label = ctk.CTkLabel(self, text='Create a New Session', font=LARGE_FONT)
		label.place(relx=0.5, rely=0.20, anchor=CENTER)

		label = ctk.CTkLabel(self, text='Please enter session name:', font=MEDIUM_FONT)
		label.place(relx=0.5, rely=0.3, anchor=CENTER)
		session_name = ctk.CTkEntry(self, width=200)
		session_name.place(relx=0.5, rely=0.35, anchor=CENTER)

		label = ctk.CTkLabel(self, text='Please select audio files:', font=MEDIUM_FONT)
		label.place(relx=0.5, rely=0.45, anchor=CENTER)

		btn_home = ctk.CTkButton(self, text ="Browse",
							command = lambda : self.upload_audio(audio))
		btn_home.place(relx = 0.5, rely = 0.50, anchor=CENTER)

		

		self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, width=75)
		self.listbox.place(relx = 0.5, rely = 0.725, anchor=CENTER)
		
		#self.scrollbar = tk.Scrollbar(self, command=self.listbox.yview)
		#self.scrollbar.place(relx=0.73, rely=0.7, anchor=CENTER)
		#self.listbox.config(yscrollcommand=self.scrollbar.set)
		
		#self.load_audio_files(audio)
			
		self.edit_button = tk.Button(self, text="Edit", 
							   command=lambda : self.edit_selected_row(audio=audio))
		self.edit_button.place(relx=0.85, rely=0.7, anchor=CENTER)
		
		self.listbox.bind('<ButtonRelease-1>', self.on_select)

		btn_home = ctk.CTkButton(self, text ="Back",
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = 0, column = 0, padx = 10, pady = 10)

		btn_OK = ctk.CTkButton(self, text = "Save",
							command = lambda : add_session(session_name.get(), audio, callback=self.clear_and_home(audio, session_name, controller)))
		btn_OK.place(relx=0.5, rely=0.95, anchor=CENTER)

	def upload_audio(self, audio):
		tk.Tk().withdraw()
		fp = askopenfilename()
		fn = os.path.basename(fp)
		
		audio.append({'path': fp, 'answer': fn})
		self.load_audio_files(audio)

	def load_audio_files(self, audio):

		for item in audio:
			print("item")
			self.listbox.insert(tk.END, item['path'] + ": " + item['answer'])
		

	def on_select(self, audio):
		selected_index = self.listbox.curselection()
		if selected_index:
			index = int(selected_index[0])
			print("Selected:", audio[index])

	def edit_selected_row(self, audio):
		print("edit")
		selected_index = self.listbox.curselection()
		if selected_index:
			index = int(selected_index[0])
			new_answer = simpledialog.askstring("Edit Answer", "Enter new answer:")
			if new_answer is not None:
				audio[index] = {'path': audio[index]['path'], 'answer' : new_answer}
				self.listbox.delete(0, tk.END)
				for item in audio:
					self.listbox.insert(tk.END, item['path'] + ": " + item['answer'])

	def clear_and_home(self, audio, session_name, controller):
		audio = []
		#self.load_audio_files(audio)
		session_name.delete(0, END)
		controller.show_frame(HomePage)


		


# consists of:
# a sidebar with a list of sessions
# a list of settings that can be edited
# a button to save/update the settings
class SettingsPage(ctk.CTkFrame):
	
	def __init__(self, parent, controller):
		#test
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

		f = open('src/sessions.json')
		data = json.load(f)
		sessionsList = list(data.keys())
		listbox_sessions = CTkListbox(height=300, width=150, master=self, text_color="black")
		listbox_sessions.place(x=200, y=200)
		for i in range(1, len(sessionsList) + 1):
			listbox_sessions.insert(i, sessionsList[i - 1])
		#remove and rename session button
		def rename_session():
			if(listbox_sessions.curselection()==None):
				return
			popup = ctk.CTkToplevel(self)
			popup.wm_title("Rename")
			popup.geometry('150x150')
			app_x = self.winfo_x()
			app_y = self.winfo_y()
			app_width = self.winfo_width()
			app_height = self.winfo_height()
			popup_width = 250
			popup_height = 200
			x = app_x + app_width // 2 - popup_width // 2
			y = app_y + app_height // 2 - popup_height // 2
			popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")  # Set popup window size and position
			inputtxt = tk.Text(popup,
                   height = 5,
                   width = 20)

			def changename():
				newname = inputtxt.get(1.0, "end-1c")
				if(newname in data):
					errormessage = ctk.CTkLabel(popup,text="No duplicate session names",text_color="red")
					errormessage.place(x=50,y=110)
				else:
					data[newname] = data[listbox_sessions.get(listbox_sessions.curselection())]
					del data[listbox_sessions.get(listbox_sessions.curselection())]
					_update_sessions_json(data)
					listbox_sessions.insert(listbox_sessions.curselection(),newname)
					listbox_sessions.delete(listbox_sessions.curselection())
					popup.destroy()
					return

			submit_btn = ctk.CTkButton(popup,text="Submit",command=changename)
			submit_btn.place(x=50,y=70)
			inputtxt.pack()
			if True:
				popup.grab_set()
				self.wait_window(popup)

		btn_remove_session = ctk.CTkButton(self, text="Remove Session",
								 command=lambda: controller.show_frame(HomePage))
		btn_remove_session.place(x=50,y=300)

		btn_rename_session = ctk.CTkButton(self, text="Rename Session",
								 command=lambda: rename_session())
		btn_rename_session.place(x=50,y=350)


		#Songs Box
		listbox_songs = CTkListbox(height=300, width=200, master=self, text_color="black")
		listbox_songs.place(x=400, y=200)
		def loadSongs(evt):
			if(listbox_sessions.selected!=None):
				print(listbox_sessions.get(listbox_sessions.curselection()))
				selsesh = data[listbox_sessions.get(listbox_sessions.curselection())]
				audfiles = selsesh['audio_files']
				for i in range(1,len(audfiles)+1):
					listbox_songs.insert(i, audfiles[i - 1]['answer'])
		listbox_sessions.bind("<Double-Button-1>", loadSongs)

		#Song option buttons
		btn_remove_song = ctk.CTkButton(self, text="Remove Song",
										   command=lambda: controller.show_frame(HomePage))
		btn_remove_song.place(x=630, y=280)

		btn_rename_song = ctk.CTkButton(self, text="Rename Song",
										   command=lambda: controller.show_frame(HomePage))
		btn_rename_song.place(x=630, y=330)

		btn_add_song = ctk.CTkButton(self, text="Add Song",
										command=lambda: controller.show_frame(HomePage))
		btn_add_song.place(x=630, y=480)

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
		replay_button = ctk.CTkButton(self, text =constants.REPLAY_BUTTON,
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
		btn_success = ctk.CTkButton(self, text =constants.SUCCESS_BUTTON,
							command = lambda : self.UpdateScore(is_success=True, callback=self.trivia.PlayNextTrack))
		btn_success.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1

		# failure
		# no points, just go to next
		btn_failure = ctk.CTkButton(self, text =constants.FAILURE_BUTTON,
							command = lambda : self.UpdateScore(is_success=False, callback=self.trivia.PlayNextTrack))
		btn_failure.grid(row = row, column = audio_button_column, padx = 10, pady = 5)
		row+=1

		# retry
		btn_retry = ctk.CTkButton(self, text =constants.RETRY_BUTTON,
							command = lambda : self.trivia.PlayDifferentInterval())
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
		self.banner_label.config(borderwidth=0)
		self.banner_label.image = banner_photo
		self.banner_label.place(relx=0.5, rely=0, anchor=N)

	def hide_banner(self):
		self.banner_label.place_forget()

	

if __name__ == '__main__':
	app = tkinterApp()
	app.mainloop()
