import sessions
import tracks

# an instance of Trivia is made every time you load a session. When you close and reopen, the score resets, etc
# when this launches, the settings are set. All this is is a mapping for the LOGIC functions needed for the frontend

class Trivia:

    # OnSessionOpened
    def __init__(self, session_name):
        self.session_name = session_name
        session_info = sessions.get_session(self.session_name)
        self.ResetScore()

        if session_info:
            self.interval_length = session_info['interval_length']
            self.start_delay = session_info['start_delay']
            self.end_delay = session_info['end_delay']
        else:
            # Handle the case where the session does not exist
            pass

    # OnNextButtonPressed / OnFailButtonPress
    def PlayNextAudio(self):
        # get the track and the start timestamp
        self.track = tracks.GetRandomAudio(self.session_name) # get a random track from the session
        self.timeStamp = tracks.GetRandomTimestamp(self.track, self.interval_length, self.start_delay, self.end_delay)

        #play the track right away
        self.track.Play(self.timeStamp, self.interval_length)

    # OnReplayButtonPressed
    def ReplayAudio(self):
        #play it again from the same timestamp
        self.track.Play(self.timeStamp, self.interval_length)

    # OnIncreaseIntervalButtonPressed
    def UpdateIntervalLength(self, interval_change):
        # if we change the interval, it will override the end_delay and keep playing to the end of the song if it needs to 
        self.interval_length += interval_change

    # OnSuccessButtonPressed
    def UpdateScore(self):
        score+=1
        self.PlayNextAudio(self.session_name)

    # used for init, do we want a reset button?
    def ResetScore(self):
        self.score=0

    def PlayDifferentInterval(self):
        # get a new timestamp and play it (same file)
        self.timeStamp = tracks.GetRandomTimestamp(self.track, self.interval_length, self.start_delay, self.end_delay)
        self.track.Play(self.timeStamp, self.interval_length)

# Example usage:
session_name = "example_session"
trivia_game = Trivia(session_name)
print(trivia_game.interval_length)  # Access session settings using trivia_game.settings
