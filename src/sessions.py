import json

"""
A module to manage sessions.
"""

SESSIONS_DB_FILENAME = 'sessions.json'

AUDIO_FILE_PATHS_KEY = 'audio_file_paths'
SETTINGS_KEY = 'settings'
INTERVAL_LENGTH_KEY = 'interval_length'
START_DELAY_KEY = 'start_delay'
END_DELAY_KEY = 'end_delay'

def add_session(session_name, audio_fpaths, interval_length=10, start_delay=0,
    end_delay=0):
    """
    Args:
        session_name (str): A string representing the name of the session.
        audio_fpaths (list[str]): A list of strings representing the paths of
            the audio associated with the session.
        interval_length (int): An integer representing the length of the
            audio to be played in seconds. Default is 10 seconds.
        start_delay (int): An integer representing the start delay. Default is
            0 seconds.
        end_delay(int): An integer representing the end delay. Default is 0
            seconds.
    """
    # get the content of sessions.json as a dict
    with open(SESSIONS_DB_FILENAME, 'r') as openfile:
        sessions_json = json.load(openfile)

    # add a new session to sessions_json
    sessions_json[session_name] = {
        AUDIO_FILE_PATHS_KEY: audio_fpaths,
        SETTINGS_KEY: {
            INTERVAL_LENGTH_KEY: interval_length,
            START_DELAY_KEY: start_delay,
            END_DELAY_KEY: end_delay
        }
    }

    # serialize json
    sessions_json = json.dumps(sessions_json, indent=4)

    # update sessions.json with the current sessions_json dict
    with open(SESSIONS_DB_FILENAME, 'w') as openfile:
        openfile.write(sessions_json)

if __name__ == '__main__':
    """
    For testing purposes.
    """
    audio_fpaths = ["audio1.mp3", "audio2.mp3"]
    add_session("testing", audio_fpaths)
