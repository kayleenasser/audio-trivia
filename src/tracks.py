import random
import time
import sessions
from pathlib import Path
from pygame import mixer

class Track:
    def __init__(self, name, track_path, interval):
        self.name = name
        self.track_path = track_path
        self.interval = interval
# Name - string
# Path - string
# Interval - int seconds 

def Play_Track(track_obj): 
    # ----- PLACEHOLDERS, DELETE LATER -------
    start_delay = 5
    end_delay = 60000
    # ----------------------------------------
    path = Path(track_obj.track_path)
    song = path / track_obj.name
    duration = int(get_track_length(song))
    try:
        start_point = random.randint(start_delay, duration - end_delay - track_obj.interval)
    except:
        start_point = random.randint(0, duration - track_obj.interval)

    mixer.init() # Starting the mixer
    mixer.music.load(song) # Loading the song
    mixer.music.set_volume(0.7)  # Setting the volume 
    mixer.music.play(start = start_point) # Starting song from second indicated
    if mixer.music.get_pos == track_obj.interval:
        mixer.music.stop()
        mixer.music.unload(song) # Unloads the song
    time.sleep(5)

def get_track_length(file_path):
    mixer.init()
    mixer.music.load(file_path)
    length_in_seconds = mixer.Sound(file_path).get_length()
    mixer.quit()
    return length_in_seconds


if __name__ == '__main__':
# ------------ MORE TEST STUFF ------------
	mypath = Path("res/test_audio/AvatarTheme.mp3")
	track_obj = Track("AvatarTheme.mp3", mypath, 5)
	Play_Track(track_obj)
# -----------------------------------------