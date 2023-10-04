# frontend.py ################################################################
APP_TITLE = "Audio Trivia"
SETTINGS = "Settings"
SESSION = "Session"
HOME = "Home"
OPEN_SESSION = "Open Session"
CREATE_SESSION = "Create Session"

# session buttons
SHOW_ANSWER = "Show Answer"
HIDE_ANSWER = "Hide Answer"
PLAY_BUTTON = "Play"
PAUSE_BUTTON = "Pause"
REPLAY_BUTTON = "Replay"

EXAMPLE_SESSIONS = [
    "default",
    "session2",
    "session3",
    "session1",
    "session2",
    "session3",
    "session1",
    "session2",
    "session3"
]

# sessions.py ################################################################
DEFAULT_SESSION_NAME = "default"
SESSIONS_DB_FILENAME = 'sessions.json'

AUDIO_FILES_KEY = 'audio_files'
ANSWER_KEY = 'answer'
SETTINGS_KEY = 'settings'
INTERVAL_LENGTH_KEY = 'interval_length'
INCREASE_AMOUNT_KEY = 'increase_amount'
START_DELAY_KEY = 'start_delay'
END_DELAY_KEY = 'end_delay'

DIRECTORY = 'src'