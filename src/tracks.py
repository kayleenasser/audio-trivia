import time
import playsound

class Audio:
    def __init__(self, name, audio_path, start_minute, start_second, duration):
        self.name = name
        self.audio_path = audio_path
        self.start_minute = start_minute
        self.start_second = start_second
        self.duration = duration

    def Play_Audio(self): 
        playsound.playsound(self.audio_path + "\\" + self.name)
        time.sleep(5)

# Name - string
# Path - string
# Time stamp min - int min 
# Time stamp second - int second 0 - 59 
# Duration - int seconds 

audio_obj = Audio("AvaterTheme.mp3", "C:\Files\Hackathon\\test-audio", 3, 40, 10)

audio_obj.Play_Audio()