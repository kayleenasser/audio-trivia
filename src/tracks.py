import random
import os
import sessions
import constants
from pathlib import Path
import pygame
from pygame import mixer
import threading

class Track:
	def __init__(self, name, filepath):
		self.name = name # filename or custom? @TODO
		self.filepath = Path(filepath)
		print(self.filepath)
		self.duration = self.GetTrackLength()
		pygame.init()

		self.playing = False
		self.play_thread = None
		
	def __del__(self):
		mixer.quit()

	def PlayThreaded(self, timestamp, interval):
		if not self.is_playing():
			self.play_thread = threading.Thread(target=self.Play, args=(timestamp, interval))
			self.play_thread.start()

	# play this track
	def GetRandomTimestamp(self, start_delay, end_delay, interval):
		print(start_delay, self.duration, end_delay, interval)
		try:
			timestamp = random.randint(start_delay, int(self.duration - end_delay - interval))
			
		except:
			print("No valid timestamp available. Ignoring delays.")
			timestamp = random.randint(0, int(self.duration - interval))

		return timestamp

	def Play(self, timestamp, interval):
		print("Playing track from: ", timestamp, " seconds.")
		self.playing = True
		mixer.init()
		mixer.music.load(self.filepath) # Loading the song
		mixer.music.set_volume(0.5)  # Setting the volume 
		mixer.music.play(start = timestamp) # Starting song from second indicated

		clock = pygame.time.Clock()
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				# Handle your button inputs here
				# For example:
				# if event.type == pygame.KEYDOWN:
				#     if event.key == pygame.K_SPACE:
				#         # Handle spacebar press
				#     elif event.key == pygame.K_ESCAPE:
				#         running = False

			# Check if the music has played for the desired interval
			current_pos = mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
			if current_pos >= interval:
				running = False

			clock.tick(30)  # Limit the frame rate to 30 FPS

		self.Stop()
		mixer.music.unload() # Unloads the song
		return True # the value can be used for is_paused? 
	
		# time.wait(int(interval * 1000))  # Wait for the specified interval in milliseconds (pygame, not os)
		#mixer.music.stop()
		# @TODO : How to update the Play/Pause button in Trivia based on the music playing/not?
		# right now just being updated by pressing the button, but we also "pause" inherently at the end of the track
		#mixer.quit()

	def Pause(self):
		self.playing = False
		mixer.music.pause()
		print("Pausing track.")

	def Resume(self):
		self.playing = True
		mixer.music.unpause()
		print("Resuming track.")

	def Stop(self):
		self.playing = False
		mixer.music.stop()
		print("Stopping track.")
	
	def is_playing(self):
		return self.playing

	# get the length of this track (INT ONLY)
	def GetTrackLength(self):
		mixer.init()
		mixer.music.load(self.filepath)
		length_in_seconds = (mixer.Sound(self.filepath).get_length())
		mixer.quit()
		return length_in_seconds


# get a random filepath from the session, and return a Track object
def GetRandomTrack(filepath_list):
	while (len(filepath_list) > 0) :

		# try getting a path
		track_number = random.randint(0, len(filepath_list)-1)
		path = Path(filepath_list[track_number])

		#if it doesn't exist, remove it from the list 
		if not os.path.exists(path):
			filepath_list.pop(track_number)
			# should also remove it from the session? and warn the user? later problem
		else: 
			# create the track and return it
			path = Path(path)
			track = Track(path.name, path)
			return track


	# all tracks are invalid
	return None
	