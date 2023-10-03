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

def _update_sessions_json(sessions_dict : dict):
    """
    Serializes the specified dict and updates sessions.json with its contents.

    Args:
        sessions_dict: A dictionary representing the contents of
            sessions.json.
    """
    sessions_obj = json.dumps(sessions_dict, indent=4)
    with open(SESSIONS_DB_FILENAME, 'w') as openfile:
        openfile.write(sessions_obj)

def get_all_sessions() -> dict:
    """
    Returns:
        dict: A dictionary containing all sessions and their associated info.
    """
    with open(SESSIONS_DB_FILENAME, 'r') as openfile:
        return json.load(openfile)

def get_session(session_name : str) -> dict:
    """
    Args:
        session_name: A string representing the name of the session to get.

    Returns:
        dict: A dictionary containing the specified session's info.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        return sessions_dict[session_name]

def add_session(session_name : str, audio_fpaths : list[str],
    interval_length=10, start_delay=0, end_delay=0):
    """
    Adds a new session to sessions.json with the specified arguments.

    Args:
        session_name: A string representing the name of the session to add.
        audio_fpaths: A list of strings representing the paths of the audio
            associated with the session.
        interval_length: An integer representing the length of the audio to be
            played in seconds. Default is 10 seconds.
        start_delay: An integer representing the start delay. Default is 0
            seconds.
        end_delay: An integer representing the end delay. Default is 0
            seconds.

    Raises:
        KeyError: If session_name already exists.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        raise KeyError(f"The session name '{session_name}' already exists. \
            Please use another name.")
    sessions_dict[session_name] = {
        AUDIO_FILE_PATHS_KEY: audio_fpaths,
        SETTINGS_KEY: {
            INTERVAL_LENGTH_KEY: interval_length,
            START_DELAY_KEY: start_delay,
            END_DELAY_KEY: end_delay
        }
    }
    _update_sessions_json(sessions_dict)

def add_audio_fpath(session_name : str, audio_fpath : str):
    """
    Adds the specified audio path to the specified session.

    Args:
        session_name: A string representing the name of the session to
            add an audio path to.
        audio_fpath: A string representing the path of the audio to add.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session = sessions_dict[session_name]
        session[AUDIO_FILE_PATHS_KEY].append(audio_fpath)
        sessions_dict[session_name] = session
    _update_sessions_json(sessions_dict)

def update_session_name(current_session_name : str, new_session_name : str):
    """
    Updates the name of a session.

    Args:
        current_session_name: A string representing the current name of the
            session.
        new_session_name: A string representing the new name of the session.
    """
    sessions_dict = get_all_sessions()
    if current_session_name in sessions_dict:
        sessions_dict[new_session_name] = sessions_dict[current_session_name]
        del sessions_dict[current_session_name]
    _update_sessions_json(sessions_dict)

def update_session_audio_fpaths(session_name : str, audio_fpaths : list[str]):
    """
    Updates the list of paths of the audio associated with the specified
    session.

    Args:
        session_name: A string representing the name of the session to update
            the paths of.
        audio_fpaths: A list of strings representing the paths of the audio
            be associated with the session.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session = sessions_dict[session_name]
        session[AUDIO_FILE_PATHS_KEY] = audio_fpaths
        sessions_dict[session_name] = session
    _update_sessions_json(sessions_dict)

def update_session_settings(session_name : str, interval_length=None,
    start_delay=None, end_delay=None):
    """
    Updates the specified session's settings using the specified arguments. If
    setting is specified as None, the specified setting will remain the same.

    Args:
        sessions_name: A string representing the name of the session to update
            the settings of.
        interval_length: An integer representing the interval length to
            update. Default is None.
        start_delay: An integer representing the start delay to update.
            Default is None.
        end_delay: An integer representing the end delay to update. Default is
            None.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session_settings = sessions_dict[session_name][SETTINGS_KEY]
        if interval_length:
            session_settings[INTERVAL_LENGTH_KEY] = interval_length
        if start_delay:
            session_settings[START_DELAY_KEY] = start_delay
        if end_delay:
            session_settings[END_DELAY_KEY] = end_delay
        sessions_dict[session_name][SETTINGS_KEY] = session_settings
    _update_sessions_json(sessions_dict)

def delete_session(session_name : str):
    """
    Deletes a session from sessions.json using the specified session name.

    Args:
        session_name: A string representing the name of the session.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        del sessions_dict[session_name]
    _update_sessions_json(sessions_dict)

def delete_audio_fpath(session_name : str, audio_fpath : str):
    """
    Deletes the specified audio path from the specified session.

    Args:
        session_name: A string representing the name of the session to delete
            an audio path from.
        audio_fpath: A string representing the path of the audio to delete.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session = sessions_dict[session_name]
        session[AUDIO_FILE_PATHS_KEY].remove(audio_fpath)
        sessions_dict[session_name] = session
    _update_sessions_json(sessions_dict)

if __name__ == '__main__':
    """
    For testing purposes.
    """
    audio_fpaths = ['audio1.mp3', 'audio2.mp3']
    add_session('test1', audio_fpaths)

    delete_session('test1')

    add_session('test2', audio_fpaths, 30, 10, 5)

    update_session_name('test2', 'test3')

    audio_fpaths = ['example1.mp3', 'example2.mp3']
    update_session_audio_fpaths('test3', audio_fpaths)

    add_audio_fpath('test3', 'example3.mp3')
    delete_audio_fpath('test3', 'example3.mp3')

    update_session_settings('test3', None, 5)
    update_session_settings('test3', 10, 10, 10)
    update_session_settings('test3', 5, None, 5)
