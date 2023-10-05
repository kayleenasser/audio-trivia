# frontend.py ################################################################
APP_TITLE = "Listen Up!"
SETTINGS = "Settings"
SESSION = "Collection"
HOME = "Home"
OPEN_SESSION = "Open Collection"
CREATE_SESSION = "Create Collection"
REMOVE_SESSION = "Remove Collection"
RENAME_SESSION = "Rename Collection"
BAD_NAME = "Sorry, you can't choose this name."
ALREADY_EXISTS = "This collection name already exists!"
FILETYPES = [
    ".mp3"
]

# session buttons
SHOW_ANSWER = "Show Answer"
HIDE_ANSWER = "Hide Answer"
REMOVE_SONG = "Remove Song"
RENAME_SONG = "Rename Song"
ADD_SONG = "Add Song"
PLAY_BUTTON = "Play"
PAUSE_BUTTON = "Pause"
OK_BUTTON = "Okay"
CLOSE_BUTTON = "Close"
EDIT_BUTTON = "Edit"
BACK_BUTTON = "Back"
SAVE_BUTTON = "Save"
DELETE_BUTTON = "Delete"
REPLAY_BUTTON = "Replay"
SUBMIT_BUTTON = "Submit"
SUCCESS_BUTTON = "Checkmark"
FAILURE_BUTTON = "X"
RETRY_BUTTON = "Retry"

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
PATH_KEY = 'path'
ANSWER_KEY = 'answer'
SETTINGS_KEY = 'settings'
INTERVAL_LENGTH_KEY = 'interval_length'
INCREASE_AMOUNT_KEY = 'increase_amount'
START_DELAY_KEY = 'start_delay'
END_DELAY_KEY = 'end_delay'

# for running locally
ASSETS_DIRECTORY = 'assets'


WELCOME_TEXT = f"Welcome to {APP_TITLE}\n Please choose how you would like to run your game!"

DEFAULT_SESSION = {
    "default": {
        "audio_files": [
            {
                "path": "res/test_audio/1-01 The Boy in the Iceberg, The Ava.mp3",
                "answer": "The Boy in the Iceberg"
            },
            {
                "path": "res/test_audio/1-03 The Southern Air Temple.mp3",
                "answer": "The Southern Air Temple"
            },
            {
                "path": "res/test_audio/1-04 The Warriors of Kyoshi.mp3",
                "answer": "The Warriors of Kyoshi"
            }
        ],
        "settings": {
            "interval_length": 5,
            "increase_amount": 3,
            "start_delay": 0,
            "end_delay": 0
        }
    }
}
