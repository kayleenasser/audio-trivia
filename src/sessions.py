import json
import os

import constants as const

"""
A module to perform CRUD operations on sessions.json.
"""

def _update_sessions_json(sessions_dict : dict):
    """
    Serializes the specified dict and updates sessions.json with its contents.

    Args:
        sessions_dict: A dictionary representing the contents of
            sessions.json.
    """
    sessions_obj = json.dumps(sessions_dict, indent=4)
    with open(os.path.join(const.DIRECTORY, const.SESSIONS_DB_FILENAME), \
        'w') as f:
        f.write(sessions_obj)

def get_all_sessions() -> dict:
    """
    Returns:
        dict: A dictionary containing all sessions and their associated info.
    """
    with open(os.path.join(const.DIRECTORY, const.SESSIONS_DB_FILENAME), \
        'r') as f:
        return json.load(f)

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


def add_session(session_name : str, audio_files : list[dict[str, str]],
    interval_length=10, increase_amount=3, start_delay=0, end_delay=0):
    """
    Adds a new session to sessions.json with the specified arguments.

    Args:
        session_name: A string representing the name of the session to add.
        audio_files: A list of dictionaries representing the audio files
            associated with the session. Each dict has a string representing
            the path of the audio file and its corresponding answer.
        interval_length: An integer representing the length of the audio to be
            played in seconds. Default is 10 seconds.
        increase_amount: An integer representing an amount to increase the
            audio interval by in seconds. Default is 3 seconds.
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
        const.AUDIO_FILES_KEY: audio_files,
        const.SETTINGS_KEY: {
            const.INTERVAL_LENGTH_KEY: interval_length,
            const.INCREASE_AMOUNT_KEY: increase_amount,
            const.START_DELAY_KEY: start_delay,
            const.END_DELAY_KEY: end_delay
        }
    }
    _update_sessions_json(sessions_dict)

def add_audio_file(session_name : str, audio_file : dict[str, str]):
    """
    Adds the specified audio file to the specified session.

    Args:
        session_name: A string representing the name of the session to
            add an audio path to.
        audio_files: A dictionary representing the audio file to add. The dict
            contains a string representing the path of the audio file and its
            corresponding answer.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session = sessions_dict[session_name]
        session[const.AUDIO_FILES_KEY].append(audio_file)
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

def update_session_audio_files(session_name : str,
    audio_files : list[dict[str, str]]):
    """
    Updates the list of audio files associated with the specified session.

    Args:
        session_name: A string representing the name of the session to update
            the paths of.
        audio_files: A list of dictionaries representing the audio files
            associated with the session. Each dict has a string representing
            the path of the audio file and its corresponding answer.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session = sessions_dict[session_name]
        session[const.AUDIO_FILES_KEY] = audio_files
        sessions_dict[session_name] = session
    _update_sessions_json(sessions_dict)

def update_session_settings(session_name : str, interval_length=None,
    increase_amount=None, start_delay=None, end_delay=None):
    """
    Updates the specified session's settings using the specified arguments. If
    setting is specified as None, the specified setting will remain the same.

    Args:
        sessions_name: A string representing the name of the session to update
            the settings of.
        interval_length: An integer representing the interval length to
            update. Default is None.
        increase_amount: An integer representing an amount to increase the
            audio interval by in seconds. Default is None.
        start_delay: An integer representing the start delay to update.
            Default is None.
        end_delay: An integer representing the end delay to update. Default is
            None.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session_settings = sessions_dict[session_name][const.SETTINGS_KEY]
        if interval_length:
            session_settings[const.INTERVAL_LENGTH_KEY] = interval_length
        if increase_amount:
            session_settings[const.INCREASE_AMOUNT_KEY] = increase_amount
        if start_delay:
            session_settings[const.START_DELAY_KEY] = start_delay
        if end_delay:
            session_settings[const.END_DELAY_KEY] = end_delay
        sessions_dict[session_name][const.SETTINGS_KEY] = session_settings
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

def delete_audio_file(session_name : str, audio_answer : str):
    """
    Deletes the audio file with the specified answer from the specified
    session.

    Args:
        session_name: A string representing the name of the session to delete
            an audio path from.
        audio_answer: A string representing the answer of the audio to delete.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session = sessions_dict[session_name]
        session_audio_files = session[const.AUDIO_FILES_KEY]
        for audio_file in session_audio_files:
            if audio_file[const.ANSWER_KEY] == audio_answer:
                session_audio_files.remove(audio_file)
                break
        session[const.AUDIO_FILES_KEY] = session_audio_files
        sessions_dict[session_name] = session
    _update_sessions_json(sessions_dict)

if __name__ == '__main__':
    """
    For testing purposes.
    """
    audio_fpaths = [
        {
            "path": "example1.mp3",
            "answer": "Example 1"
        },
        {
            "path": "example2.mp3",
            "answer": "Example 2"
        }
    ]
    add_session('test1', audio_fpaths)

    delete_session('test1')

    add_session('test2', audio_fpaths, 30, 20, 10, 5)

    update_session_name('test2', 'test3')

    audio_fpaths = [
        {
            "path": "test1.mp3",
            "answer": "Test 1"
        },
        {
            "path": "test2.mp3",
            "answer": "Test 2"
        }
    ]
    update_session_audio_files('test3', audio_fpaths)

    add_audio_file('test3', {"path": "test3.mp3", "answer": "Test 3"})
    delete_audio_file('test3', "Test 2")

    update_session_settings('test3', None, 5, None, 5)
    update_session_settings('test3', 10, 10, 10, 10)
    update_session_settings('test3', 5, None, 5, 10)
