import time
import sessions
from pathlib import Path
from pygame import mixer

class Audio:
    def __init__(self, name, audio_path, start_minute, start_second, duration):
        self.name = name
        self.audio_path = audio_path
        self.start_minute = start_minute
        self.start_second = start_second
        self.duration = duration

    def Play_Audio(self): 
        path = Path(self.audio_path)
        song = path / self.name
        start_point = (self.start_minute * 60) + self.start_second

        mixer.init() # Starting the mixer
        mixer.music.load(song) # Loading the song
        mixer.music.set_volume(0.7)  # Setting the volume 
        mixer.music.play(start = start_point) # Starting song from second indicated
        if mixer.music.get_pos == self.duration:
            mixer.music.stop()
            mixer.music.unload(song) # Unloads the song
        time.sleep(5)
        

# Name - string
# Path - string
# Time stamp min - int min 
# Time stamp second - int second 0 - 59 
# Duration - int seconds 
# Format - string 

# ----- Test stuff ------
mypath = Path("C:/Files/Hackathon/res/test_audio/")
audio_obj = Audio("AvatarTheme.mp3", mypath, 0, 15, 5)
audio_obj.Play_Audio()