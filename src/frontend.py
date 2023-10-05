import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import util

import sys
from ctypes import windll # Only exists on windows.

import CTkListbox

import constants as constants
import customtkinter as ctk
from CTkListbox import *
import trivia
import sessions
import os
import tracks
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
#fg_color="#2BCDEC", font=('Verdana', 16, "bold"),
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
			command= lambda: controller.show_frame(SettingsPage),height= 30, width=50)
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

		self.selected_track = []

		label = ctk.CTkLabel(self, text='Create a New Collection', font=LARGE_FONT)
		label.place(relx=0.5, rely=0.20, anchor=CENTER)

		label = ctk.CTkLabel(self, text='Please enter collection name:', font=MEDIUM_FONT)
		label.place(relx=0.5, rely=0.3, anchor=CENTER)
		self.session_name = ctk.CTkEntry(self, width=200)
		self.session_name.place(relx=0.5, rely=0.35, anchor=CENTER)

		label = ctk.CTkLabel(self, text='Please select audio files:', font=MEDIUM_FONT)
		label.place(relx=0.5, rely=0.45, anchor=CENTER)

		btn_home = ctk.CTkButton(self, text ="Browse",
							command = lambda : self.upload_audio(self.selected_track))
		btn_home.place(relx = 0.5, rely = 0.50, anchor=CENTER)

		# track list
		self.listbox_tracks = CTkListbox(height=200, width=600, master=self, command= self.on_select)
		self.listbox_tracks.place(relx = 0.5, rely = 0.725, anchor=CENTER)
		
		# buttons
		self.edit_button = ctk.CTkButton(self, text=constants.EDIT_BUTTON, 
					   command=lambda : self.edit_selected_row(audio=self.selected_track))
		self.edit_button.place(relx=0.25, rely=0.95, anchor=CENTER)

		self.delete_button = ctk.CTkButton(self, text=constants.DELETE_BUTTON, 
					   command=lambda : self.delete_selected_row(audio=self.selected_track))
		self.delete_button.place(relx=0.5, rely=0.95, anchor=CENTER)

		btn_home = ctk.CTkButton(self, text =constants.BACK_BUTTON,
							command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = 0, column = 0, padx = 10, pady = 10)

		btn_OK = ctk.CTkButton(self, text =constants.SAVE_BUTTON,
							command = lambda : add_session(self.session_name.get(), self.selected_track, controller, callback=self.clear_and_home))
		btn_OK.place(relx=0.75, rely=0.95, anchor=CENTER)

	def upload_audio(self, audio):
		tk.Tk().withdraw()
		fp = askopenfilename()
		fn = os.path.basename(fp)
		
		print(os.path.splitext(fn)[1])
		print(constants.FILETYPES)

		if (os.path.splitext(fn)[1] not in constants.FILETYPES):
			messagebox.showerror('Invalid Filetype', 'Error: The filetype that was selected is invalid.')
			return
		
		for item in audio:
			if (fp == item['path']):
				messagebox.showerror('Duplicate File', 'Error: This file was already added to the session.')
				return

		audio.append({'path': fp, 'answer': fn})
		#self.listbox_tracks.insert(tk.END, fp + ": " + fn)
		self.listbox_tracks.insert(tk.END, f"Answer: {fn}, Path: {fp}")

	def on_select(self, audio):
		print(audio)
		selected_index = self.listbox_tracks.curselection()
		if selected_index:
			index = int(selected_index[0])
			print("Selected:", audio[index])

	def edit_selected_row(self, audio):
		selected_index = self.listbox_tracks.curselection()
		if selected_index != None:
			print("Rename track")

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
				audio[selected_index] = {'path': audio[selected_index]['path'], 'answer' : new_name}
				self.listbox_tracks.delete(0, tk.END)
				for item in audio:
					self.listbox_tracks.insert(tk.END, f"Answer: {item['answer']}, Path: {item['path']}")
				popup.destroy()

			submit_btn = ctk.CTkButton(popup, text=constants.SUBMIT_BUTTON, command=ChangeSessionName)
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
	

	def delete_selected_row(self, audio):
		selected_index = self.listbox_tracks.curselection()
		if selected_index != None:
			print(selected_index)
			print(audio)
			del audio[selected_index]
			self.listbox_tracks.delete(0, tk.END)
			for item in audio:
				self.listbox_tracks.insert(tk.END, f"Answer: {item['answer']}, Path: {item['path']}")

	def clear_and_home(self, audio, controller):
		self.listbox_tracks.delete(0, tk.END)
		self.session_name.delete(0, END)
		audio.clear()
		controller.show_frame(HomePage)


		


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

		ctk.CTkFrame.__init__(self, parent)
		# title label
		label = ctk.CTkLabel(self, text=constants.SETTINGS, font=LARGE_FONT)
		label.place(relx=0.5, rely=0.075, anchor=N)

		# Switch to HOME
		btn_home = ctk.CTkButton(self, text =constants.BACK_BUTTON, command = lambda : controller.show_frame(HomePage))
		btn_home.grid(row = 0, column = 0, padx = 10, pady = 10)


		# get the sessions from the json
		# load them into the listbox
		self.UpdateSessionsList()
		self.listbox_sessions = CTkListbox(height=300, width=200, master=self, command=self.LoadAnswers)
		self.listbox_sessions.place(relx=0.05, rely=0.45, anchor=W)
		for i in range(0, len(self.sessions_list)):
			self.listbox_sessions.insert(i, self.sessions_list[i])

		#Songs Box
		self.listbox_tracks = CTkListbox(height=300, width=200, master=self,command=self.SelectTrackCallback)
		self.listbox_tracks.place(relx=0.5, rely=0.45, anchor=CENTER)

		#add ui for globalsettings (interval length, etc) as a third column beside the listboxes
		interval_label = ctk.CTkLabel(self, text="Interval Length", font=MEDIUM_FONT)
		interval_label.place(relx=0.85, rely=0.25, anchor=E)

		interval_label = ctk.CTkLabel(self, text="Delay from Start", font=MEDIUM_FONT)
		interval_label.place(relx=0.85, rely=0.35, anchor=E)

		interval_label = ctk.CTkLabel(self, text="Delay from End", font=MEDIUM_FONT)
		interval_label.place(relx=0.85, rely=0.45, anchor=E)

		interval_label = ctk.CTkLabel(self, text="Increase Time Amount", font=MEDIUM_FONT)
		interval_label.place(relx=0.9, rely=0.55, anchor=E)

		current_value1 = tk.DoubleVar()
		current_value2 = tk.DoubleVar()
		current_value3 = tk.DoubleVar()
		def get_current_value1():
			return '{: .2f}'.format(current_value1.get())
		def get_current_value2():
			return '{: .2f}'.format(current_value2.get())
		def get_current_value3():
			return '{: .2f}'.format(current_value3.get())

		def slider_changed1(event):
			value_int_slider.configure(text=get_current_value1())
		
		def slider_changed2(event):
			value_label_delay_start.configure(text=get_current_value2())

		def slider_changed3(event):
			value_label_delay_end.configure(text=get_current_value3())


		self.interval_slider = ctk.CTkSlider(self, width=200, height=20, from_=0, to=100, command=slider_changed1,
    variable=current_value1)
		self.interval_slider.place(relx=0.9, rely=0.3, anchor=E)
		self.delay_from_start = ctk.CTkSlider(self,width=200, height=20, from_=0, to=100, command=slider_changed2,
    variable=current_value2)
		self.delay_from_start.place(relx=0.9, rely=0.4, anchor=E)
		self.delay_from_end = ctk.CTkSlider(self, width=200, height=20, from_=0, to=100, command=slider_changed3,
    variable=current_value3)
		self.delay_from_end.place(relx=0.9, rely=0.5, anchor=E)
		self.increase_amount = ctk.CTkTextbox(self, width=200, height=20)
		self.increase_amount.insert("0.1", "Enter value")
		self.increase_amount.place(relx=0.9, rely=0.62, anchor=E)

		btn_apply_settings = ctk.CTkButton(self, text="Apply Settings")
		btn_apply_settings.place(relx=0.85, rely=0.775, anchor=SE)

		value_int_slider = ctk.CTkLabel(self, text=get_current_value1())
		value_int_slider.place(relx=0.95, rely=0.3, anchor=E)
		value_label_delay_start = ctk.CTkLabel(self, text=get_current_value2())
		value_label_delay_start.place(relx=0.95, rely=0.4, anchor=E)
		value_label_delay_end = ctk.CTkLabel(self, text=get_current_value3())
		value_label_delay_end.place(relx=0.95, rely=0.5, anchor=E)

		# Other buttons
		btn_remove_session = ctk.CTkButton(self, text=constants.REMOVE_SESSION,
								 command=lambda: self.RemoveSession())
		btn_remove_session.place(relx=0.1, rely=0.775, anchor=SW)

		btn_rename_session = ctk.CTkButton(self, text=constants.RENAME_SESSION,
								 command=lambda: self.RenameSession())
		btn_rename_session.place(relx=0.1, rely=0.85, anchor=SW)

		btn_create_session = ctk.CTkButton(self, text=constants.CREATE_SESSION,
								 command=lambda: controller.show_frame(CreateSessionPage))
		btn_create_session.place(relx=0.1, rely=0.925, anchor=SW)

		#Song option buttons
		btn_remove_song = ctk.CTkButton(self, text=constants.REMOVE_SONG,
										   command=lambda: self.RemoveSong())
		btn_remove_song.place(relx=0.5, rely=0.775, anchor=S)

		btn_rename_song = ctk.CTkButton(self, text=constants.RENAME_SONG,
										   command=lambda: controller.show_frame(HomePage))
		btn_rename_song.place(relx=0.5, rely=0.85, anchor=S)

		btn_add_song = ctk.CTkButton(self, text=constants.ADD_SONG,
										command=lambda: controller.show_frame(HomePage))
		btn_add_song.place(relx=0.5, rely=0.925, anchor=S)

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
		if len(self.session_track_answers) == 0:
			self.ClearTrackList()
		else:
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
					error_message.configure(text=constants.BAD_NAME)
				else:
					error_message.configure(text=constants.ALREADY_EXISTS)
			else:
				old_name = selected_session_name
				sessions.update_session_name(old_name, new_name)
				self.ReloadSessionListbox()
				popup.destroy()

		submit_btn = ctk.CTkButton(popup, text=constants.SUBMIT_BUTTON, command=ChangeSessionName)
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
		# don't exclude the default from the list
		self.sessions_list = list(sessions.get_all_sessions().keys())
		print(self.sessions_list)

	def UpdateTrackList(self):
		print("UpdateTrackList")
		# exclude the default from the list
		self.session_track_answers = []
		util.extract_data_from_json(sessions.get_session(self.selected_session),
											constants.ANSWER_KEY,
											values=self.session_track_answers)

	def ReloadSessionListbox(self):
			if self.listbox_sessions.size() > 0:
				self.listbox_sessions.delete(0, tk.END)
				self.UpdateSessionsList()
				self.ClearTrackList()
				for i in range(0, len(self.sessions_list)):
					self.listbox_sessions.insert(i, self.sessions_list[i])

	def ClearTrackList(self):
		self.session_track_paths = []
		self.session_track_answers = []
		if self.listbox_tracks.size() > 0:
			self.listbox_tracks.delete(0, tk.END)
	
	def ReloadTrackListbox(self):
			print("ReloadTrackList")
			self.UpdateTrackList()
			self.ClearTrackList()
			self.ReloadTrackListbox()
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

		self.lbl_title = ctk.CTkLabel(self, text=sessionName, font=LARGE_FONT)
		self.lbl_title.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

		self._score = StringVar()
		self._score.set("Score: 0")
		lbl_score = ctk.CTkLabel(self, textvariable=self._score,
			font=MEDIUM_FONT)
		lbl_score.place(relx=0.95, rely=0.05, anchor=ctk.NE)

		self._track_count = 1
		self._lbl_track_count = ctk.CTkLabel(self, text='Track #1',
			font=MEDIUM_FONT)
		self._lbl_track_count.place(relx=0.95, rely=0.1, anchor=ctk.NE)

		# NAV BUTTONS ########################################################
		# switch to HOME
		btn_home = ctk.CTkButton(self, text=constants.HOME, 
			command= lambda:controller.show_frame(HomePage), height=25,
			width=80)
		btn_home.place(relx=0.05, rely=0.05, anchor=ctk.NW)

		# switch to SETTINGS
		btn_settings = ctk.CTkButton(self, text=constants.SETTINGS, 
			command= lambda:controller.show_frame(SettingsPage), height=25,
			width=80)
		btn_settings.place(relx=0.05, rely=0.1, anchor=ctk.NW)

		# GAMEPLAY BUTTONS ###################################################
		# play/pause
		# self._is_paused = True # paused, need to press play for audio

		# use this to prevent yay or nay button use until audio has played
		self._track_has_played = False

		# btn_play = ctk.CTkButton(self, text=constants.PLAY_BUTTON,
		# 	command=lambda: self._toggle_state([self._is_paused], btn_play,
		# 	constants.PLAY_BUTTON, constants.PAUSE_BUTTON,
		# 	self._update_play_toggle, self._trivia.PlayPauseTrack))
		# btn_play.place(relx=0.4, rely=0.3, anchor=ctk.E)

		# for both play and replay
		btn_replay = ctk.CTkButton(self, text=constants.REPLAY_BUTTON,
			command=lambda: self._play_button_pressed())
		btn_replay.place(relx=0.3, rely=0.3, anchor=ctk.W)

		# increase interval
		self._btn_increase = ctk.CTkButton(self, text='+3 secs.',
			command=lambda: self._increase_interval_length(), state=DISABLED)
		self._btn_increase.place(relx=0.7, rely=0.3, anchor=ctk.E)

		self._lbl_audio_length = ctk.CTkLabel(self, text=SMALL_FONT)
		self._lbl_audio_length.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
		
		# toggle value when pressed and show/hide the answer label
		self._is_answer_showing = False
		self._btn_answer = ctk.CTkButton(self, text=constants.SHOW_ANSWER,
			command=lambda: self._toggle_state([self._is_answer_showing],
			self._btn_answer, constants.HIDE_ANSWER, constants.SHOW_ANSWER,
			self._update_answer_toggle, self._show_hide_answer),
			state=DISABLED)
		self._btn_answer.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

		# this will change and can't be initialized once, so will have to move
		# to a callback probably? we'll see 
		# self._answer = trivia.GetAnswer()
		self._lbl_answer = ctk.CTkLabel(self, text='', font=SMALL_FONT)
		self._lbl_answer.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

		# success (add point to score, go to next)
		self._btn_success = ctk.CTkButton(self, text=constants.SUCCESS_BUTTON,
			command=lambda: self._success_or_failure_button_pressed(),
			state=DISABLED)
		self._btn_success.place(relx=0.3, rely=0.7, anchor=ctk.W)

		# failure (no point, go to next)
		self._btn_failure = ctk.CTkButton(self, text=constants.FAILURE_BUTTON,
			command=lambda: self._success_or_failure_button_pressed(False),
			state=DISABLED)
		self._btn_failure.place(relx=0.7, rely=0.7, anchor=ctk.E)

		# retry
		self._btn_retry = ctk.CTkButton(self, text=constants.RETRY_BUTTON,
			command=lambda: self._trivia.PlayDifferentInterval(),
			state=DISABLED)
		self._btn_retry.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)
	
	def _play_button_pressed(self):
		if not self._track_has_played:
			# if first time opening, need to Play
			self._trivia.PlayNextTrack()
			self._track_has_played = True
			# enable all buttons once audio is finished playing
			time.sleep(self._trivia.get_interval_length())
			self._btn_increase.configure(state=NORMAL)
			self._btn_answer.configure(state=NORMAL)
			self._btn_success.configure(state=NORMAL)
			self._btn_failure.configure(state=NORMAL)
			self._btn_retry.configure(state=NORMAL)
		else:
			# here we're replaying
			self._trivia.ReplayTrack()

	# for play/pause and show/hide answer
	# need to make it a list so that it's mutable
	def _toggle_state(self, state_list, button, true_text, false_text,
		updater, callback):
		state_list[0] = not state_list[0]
		# Toggle the state
		if state_list[0]:
			button.configure(text=true_text)
		else:
			button.configure(text=false_text)

		# pass the current state to a function
		if updater:
			updater(state_list[0], callback)
	
	def _update_play_toggle(self, is_paused, callback):
		self._is_paused = is_paused
		# the first time (or rather, every time) it plays the track, update
		# the one has been played. (this is to ensure we don't add score
		# before it's been played.)
		if not self._is_paused:
			self._track_has_played = True
		if callback:
			callback(self._is_paused)

	def _update_answer_toggle(self, is_answer_showing, callback):
		self._is_answer_showing = is_answer_showing
		if callback:
			callback(self._is_answer_showing)
	
	def _update_score(self, is_success, callback):
		if self._track_has_played:
			if is_success:
				self._trivia.UpdateScore()
				self._score.set(f'{self._trivia.GetScore()} points')
				 # update score immediately before continuing
				app.update_idletasks()

			#update the counter
			self._increase_track_count()
			# typically play next song
			if callback:
				callback()
			
	def _show_hide_answer(self, is_answer_showing):
		if is_answer_showing:
			self._answer = self._trivia.GetAnswer()
			self._lbl_answer.configure(text=self._answer)
		else:
			self._lbl_answer.configure(text='')

	def _increase_interval_length(self):
		self._trivia.IncreaseIntervalLength()
		self._update_lbl_audio_length()
	
	def _update_lbl_audio_length(self):
		self._lbl_audio_length.configure(
			text=f'Audio Length: {self._trivia.get_interval_length()} sec.')

	def _increase_track_count(self):
		self._track_count += 1
		self._lbl_track_count.configure(text=f'Track #{self._track_count}')

	def _success_or_failure_button_pressed(self, is_success=True):
		"""
		Args:
			is_success: True, if the success button was pressed. False, if
				not. Default is True.
		"""
		self._update_score(is_success=is_success,
			callback=self._trivia.PlayNextTrack)
		self._update_lbl_audio_length()

	def initialize_trivia(self, session_name):
		# check if trivia instance is already created
		if not (hasattr(self, 'trivia')):
			# create Trivia instance here
			self._trivia = trivia.Trivia(session_name)  
		else:
			# reset when reopening SessionPage
			self._trivia.Reset(session_name)
		
		# reset/update buttons, labels, & score
		self._score.set(f'Score: {self._trivia.GetScore()}')
		self._track_count = 1
		self._lbl_track_count.configure(text=f'Track #{self._track_count}')
		# update the value once it's been initialized
		self._btn_increase.configure(text= \
			f'+{self._trivia.GetIncreaseAmount()} sec.')
		self._lbl_audio_length.configure(
			text=f'Audio Length: {self._trivia.get_interval_length()} sec.')
		self._is_answer_showing = False
		self._track_has_played = False
		app.update_idletasks() # force update


class tkinterApp(ctk.CTk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):

		ctk.CTk.__init__(self, *args, **kwargs)

		try:
			# setting icon in taskbar
			myappid = "Magnet.Listen-Up!.1.0"
			windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
		except ImportError:
			pass

		
		ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
		ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
		self.after(201, lambda :self.iconbitmap(assets_path('icon.ico')))
		# Setup
		self.title(constants.APP_TITLE)
		self.geometry('800x600') #widthxheight

		self.after(201, lambda :app.iconbitmap(assets_path('icon.ico')))

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
	def resource_path(relative_path):
		try:
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.dirname(__file__)

		return os.path.join(base_path, relative_path)
	# change pages
	def show_frame(self, cont, *args):
		frame = self.frames[cont]

		if cont == HomePage:
			self.initialize_banner()
		else:
			self.hide_banner()

		if cont == SessionPage:
			frame.initialize_trivia(self.session_name)  # Initialize Trivia instance before showing SessionPage
			frame.lbl_title.configure(text=f'Session: {self.session_name}')
		
		if cont == SettingsPage:
			frame.ReloadSessionListbox()
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
		button = ctk.CTkButton(popup, text=constants.CLOSE_BUTTON, command=popup.destroy)
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
		okay_button = ctk.CTkButton(popup, text=constants.OK_BUTTON, command=lambda: on_select())
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
		banner = Image.open(assets_path("dark-bg.PNG"))
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
