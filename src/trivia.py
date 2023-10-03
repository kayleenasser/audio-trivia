import sessions
import tracks

# an instance of Trivia is made every time you load a session. When you close and reopen, the score resets, etc
# when this launches, the settings are set. All this is is a mapping for the LOGIC functions needed for the frontend

class Trivia:

    # OnSessionOpened
    def __init__(self, session_name):
        self.session_name = session_name
        self.ResetScore()

        try:
            session_info = sessions.get_session(self.session_name)
            print(session_info)
            if session_info:
                self.interval_length = session_info['settings']['interval_length']
                self.start_delay = session_info['settings']['start_delay']
                self.end_delay = session_info['settings']['end_delay']
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
        # get the track and the start timestamp
        self.track = tracks.GetRandomTrack(self.session_name) # get a random track from the session (name)
        self.timeStamp = tracks.GetRandomTimestamp(self.track, self.interval_length, self.start_delay, self.end_delay)

        #play the track right away
        self.track.Play(self.timeStamp, self.interval_length)

    # OnPlayPauseButtonPressed
    # should just pass in the current value of the boolean and use that i think?
    def PlayPauseTrack(self, isPaused):
        print(isPaused)

    # OnReplayButtonPressed
    def ReplayTrack(self):
        #play it again from the same timestamp
        self.track.Play(self.timeStamp, self.interval_length)

    # OnIncreaseIntervalButtonPressed
    def UpdateIntervalLength(self, interval_change):
        # if we change the interval, it will override the end_delay and keep playing to the end of the song if it needs to 
        self.interval_length += interval_change

    def GetAnswer(self):
        return self.track.name # or other success criteria

    # OnSuccessButtonPressed
    def UpdateScore(self):
        score+=1
        self.PlayNextTrack(self.session_name)

    # used for init, do we want a reset button?
    def ResetScore(self):
        self.score=0

    def PlayDifferentInterval(self):
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
    