import random
import time
import os
import sessions
from pathlib import Path
from pygame import mixer

class Track:
	def __init__(self, name, filepath):
		self.name = name # filename or custom?
		self.filepath = Path(filepath)
		print(self.filepath)
		self.name = self.filepath.name
		self.duration = self.GetTrackLength()

	# play this track
	def PlayTrack(self, start_delay, end_delay, interval):
		print(start_delay, self.duration, end_delay, interval)
		try:
			start_point = random.randint(start_delay, (self.duration - end_delay - interval))
			
		except:
			print("No valid timestamp available. Ignoring delays.")
			start_point = random.randint(0, int(self.duration - interval))

		print("Playing track from: ", start_point, " seconds")

		mixer.init() # Starting the mixer
		mixer.music.load(self.filepath) # Loading the song
		mixer.music.set_volume(0.7)  # Setting the volume 
		mixer.music.play(start = start_point) # Starting song from second indicated
		if mixer.music.get_pos == interval:
			mixer.music.stop()
			mixer.music.unload(self.filepath) # Unloads the song
		time.sleep(interval)

	# get the length of this track (INT ONLY)
	def GetTrackLength(self):
		mixer.init()
		mixer.music.load(self.filepath)
		length_in_seconds = (mixer.Sound(self.filepath).get_length())
		mixer.quit()
		return length_in_seconds



# get a random filepath from the session, and return a Track object
	def GetRandomTrack(self, filepath_list):
		while (filepath_list.len() > 0) :

			# try getting a path
			track_number = random.randint(0, filepath_list.len())
			path = filepath_list[track_number]

			#if it doesn't exist, remove it from the list 
			if not os.path.exists(path):
				filepath_list.remove(track_number)
				# should also remove it from the session? and warn the user? later problem
			else: 
				# create the track and return it
				path = Path(path)
				return Track(path.name, path)
						
			# load session data
			return track
		# all tracks are invalid
		return None
	

if __name__ == '__main__':
# ------------ MORE TEST STUFF ------------
	mypath = Path("res/test_audio/1-01 The Boy in the Iceberg, The Ava.mp3")
	track = Track(mypath.name, mypath)
	print(track)
	track.PlayTrack(0,0,10)
# -----------------------------------------