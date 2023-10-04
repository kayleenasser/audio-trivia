import random
import os
import sessions
import constants
from pathlib import Path
from pygame import time
from pygame import mixer

class Track:
	def __init__(self, name, filepath):
		self.name = name # filename or custom?
		self.filepath = Path(filepath)
		print(self.filepath)
		self.name = self.filepath.name
		self.duration = self.GetTrackLength()

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
		mixer.init() # Starting the mixer
		mixer.music.load(self.filepath) # Loading the song
		mixer.music.set_volume(0.7)  # Setting the volume 
		mixer.music.play(start = timestamp) # Starting song from second indicated
		if mixer.music.get_pos == interval:
			mixer.music.stop()
			mixer.music.unload(self.filepath) # Unloads the song
		time.wait(int(interval * 1000))  # Wait for the specified interval in milliseconds (pygame, not os)
		mixer.music.stop()
		mixer.quit()

	def Stop(self):
		print("Stopping Track (placeholder)")

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
		print ()
		track_number = random.randint(0, len(filepath_list)-1)
		path = Path(filepath_list[track_number])
		print(track_number)

		#if it doesn't exist, remove it from the list 
		if not os.path.exists(path):
			filepath_list.pop(track_number)
			# should also remove it from the session? and warn the user? later problem
		else: 
			# create the track and return it
			path = Path(path)
			track = Track(path.name, path)
			print(track)
			return track


	# all tracks are invalid
	return None
	

if __name__ == '__main__':
# ------------ MORE TEST STUFF ------------
	mypath = Path("res/test_audio/1-01 The Boy in the Iceberg, The Ava.mp3")

	track_list = sessions.get_session(constants.DEFAULT_SESSION_NAME)[constants.AUDIO_FILE_PATHS_KEY]

	track = GetRandomTrack(track_list)

	print(track)
	if track:
		interval = 5
		track.Play(track.GetRandomTimestamp(0,0,interval),interval)
# -----------------------------------------