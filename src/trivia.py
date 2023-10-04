import sessions
import tracks
import constants

# an instance of Trivia is made every time you load a session. When you close and reopen, the score resets, etc
# when this launches, the settings are set. All this is is a mapping for the LOGIC functions needed for the frontend

class Trivia:

    # OnSessionOpened
    def __init__(self, session_name):
        self.session_name = session_name
        self.ResetScore()

        # @TODO add this to settings! 
        self.increase_amount = 5 

        try:
            session_info = sessions.get_session(self.session_name)
            print(session_info)
            if session_info:
                self.interval_length = session_info[constants.SETTINGS_KEY][constants.INTERVAL_LENGTH_KEY]
                self.start_delay = session_info[constants.SETTINGS_KEY][constants.START_DELAY_KEY]
                self.end_delay = session_info[constants.SETTINGS_KEY][constants.END_DELAY_KEY]
                self.track_list = session_info[constants.AUDIO_FILE_PATHS_KEY]
                self.ResetScore()
            else:
                raise SessionNotFoundError(f"Session '{session_name}' not found.")
        except SessionNotFoundError as e:
            print(f"Error: {e}")
            # Handle the error, show an error message to the user, or return an error response to the frontend
            # You can also raise the exception again if you want to handle it at a higher level in your code
            # raise e

    # OnNextButtonPressed / OnFailButtonPress
    def PlayNextTrack(self):
        print("PlayNextTrack.")
        # get the track and the start timestamp
        self.track = tracks.GetRandomTrack(self.track_list) # get a random track from the session (name)
        self.timeStamp = self.track.GetRandomTimestamp(self.start_delay, self.end_delay, self.interval_length)

        print(self.track)

        #play the track right away
        self.track.Play(self.timeStamp, self.interval_length)

    # OnPlayPauseButtonPressed
    # currently just restarts doesn't resume (need a tracker for progress)
    def PlayPauseTrack(self, isPaused):
        print("paused? ", isPaused)
        if not isPaused:
            if not hasattr(self, 'track'):
                self.PlayNextTrack()
            else:
                self.ReplayTrack() #will resume instead
        else:
            self.track.Stop()
            
        print("PlayPauseTrack. isPaused: ", isPaused)

    # OnReplayButtonPressed
    def ReplayTrack(self):
        print("ReplayTrack.")
        #play it again from the same timestamp
        self.track.Play(self.timeStamp, self.interval_length)

    # OnIncreaseIntervalButtonPressed
    def IncreaseIntervalLength(self):
        print("UpdateIntervalLength.")
        # if we change the interval, it will override the end_delay and keep playing to the end of the song if it needs to 
        self.interval_length += self.increase_amount

    def GetAnswer(self):
        return "self.track.name" #self.track.name # or other success criteria
    
    def GetIncreaseAmount(self):
        return self.increase_amount

    # OnSuccessButtonPressed
    def UpdateScore(self):
        print("UpdateScore.")
        self.score+=1
        self.PlayNextTrack()
    
    def GetScore(self):
        return self.score

    # used for init, do we want a reset button?
    def ResetScore(self):
        print("ResetScore.")
        self.score=0

    # OnRetryTrackButtonPressed
    # when you want to try the same track again from a different spot
    def PlayDifferentInterval(self):
        print("PlayDifferentInterval.")
        # get a new timestamp and play it (same file)
        self.timeStamp = tracks.GetRandomTimestamp(self.track, self.interval_length, self.start_delay, self.end_delay)
        self.track.Play(self.timeStamp, self.interval_length)

# ERRORS
class SessionNotFoundError(Exception):
    pass

# Example usage:
# if __name__ == '__main__':
#     session_name = "example_session"
#     trivia_game = Trivia(session_name)
#     print(trivia_game.interval_length)  # Access session settings using trivia_game.settings
    