import json
import os
import time
import sys
from tkinter import messagebox

import constants as const

"""
A module to perform CRUD operations on sessions.json.
"""
def assets_path(relative_path):
		try:
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.join(os.path.dirname(__file__), const.ASSETS_DIRECTORY)

		return os.path.join(base_path, relative_path)

def get_path(relative_path):
		try:
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.dirname(__file__)

		return os.path.join(base_path, relative_path)

def _update_sessions_json(sessions_dict : dict):
    """
    Serializes the specified dict and updates sessions.json with its contents.

    Args:
        sessions_dict: A dictionary representing the contents of
            sessions.json.
    """
    sessions_obj = json.dumps(sessions_dict, indent=4)
    with open(get_path(const.SESSIONS_DB_FILENAME), \
        'w') as f:
        f.write(sessions_obj)

def default_sessions_json():
    """
    Resets sessions.json with default session.
    """
    _update_sessions_json(const.DEFAULT_SESSION)

def get_all_sessions(include_default=True) -> list[dict]:
    """
    Args:
        include_default: True, if default session is to be returned. False, if
            not. Default is True.

    Returns:
        list[dict]: A list of dictionaries containing all sessions and their
            associated info.
    """
    with open(get_path(const.SESSIONS_DB_FILENAME), \
        'r') as f:
        sessions_dict = json.load(f)
        if not include_default:
            del sessions_dict[const.DEFAULT_SESSION_NAME]
        return sessions_dict

def get_num_sessions(include_default=True) -> int:
    """
    Args:
        include_default: True, if default session is to be included in the
            count. False, if not. Default is True.
        
    Returns:
        int: An integer representing the number of sessions in sessions.json.
    """
    return len(get_all_sessions(include_default))

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


def add_session(session_name : str, audio_files : list[dict[str, str]], controller, callback):
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
        messagebox.showerror('Invalid Collection Name', "The collection name '" + session_name + "' already exists. Please use another name.")
        return
    if (audio_files == []):
        #raise KeyError(f"No audio files were added to the session. \
        #    Please add 1 or more audio files to the session.")
        messagebox.showerror('Error', 'Error: No audio files were added to the collection. Please add 1 or more audio files to the collection before saving.')
        return
    
    sessions_dict[session_name] = {
        const.AUDIO_FILES_KEY: audio_files,
        const.SETTINGS_KEY: {
            const.INTERVAL_LENGTH_KEY: sessions_dict[const.DEFAULT_SESSION_NAME][const.SETTINGS_KEY][const.INTERVAL_LENGTH_KEY],
            const.INCREASE_AMOUNT_KEY: sessions_dict[const.DEFAULT_SESSION_NAME][const.SETTINGS_KEY][const.INCREASE_AMOUNT_KEY],
            const.START_DELAY_KEY: sessions_dict[const.DEFAULT_SESSION_NAME][const.SETTINGS_KEY][const.START_DELAY_KEY],
            const.END_DELAY_KEY: sessions_dict[const.DEFAULT_SESSION_NAME][const.SETTINGS_KEY][const.END_DELAY_KEY]
        }
    }
    _update_sessions_json(sessions_dict)

    if (callback):
        callback(audio_files, controller)

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
    
def update_session_audio_answer(session_name: str, path: str, new_answer: str):
    """
    Updates the answer of a specific audio file associated with the specified session.

    Args:
        session_name: A string representing the name of the session to update the audio file in.
        path: A string representing the path of the audio file to be updated.
        new_answer: A string representing the new answer for the specified audio file.
    """
    sessions_dict = get_all_sessions()

    if session_name in sessions_dict:
        session = sessions_dict[session_name]
        audio_files = session.get(const.AUDIO_FILES_KEY, [])

        # Iterate through audio_files and update the answer for the specified path
        for audio_file in audio_files:
            if audio_file.get("path") == path:
                audio_file["answer"] = new_answer

        # Update the sessions dictionary with the modified audio_files list
        session[const.AUDIO_FILES_KEY] = audio_files
        sessions_dict[session_name] = session

        # Update the JSON file
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

def delete_audio_file(session_name : str, audio_path : str):
    """
    Deletes the audio file with the specified answer from the specified
    session.

    Args:
        session_name: A string representing the name of the session to delete
            an audio path from.
        audio_path: A string representing the path of the audio to delete.
    """
    sessions_dict = get_all_sessions()
    if session_name in sessions_dict:
        session = sessions_dict[session_name]
        session_audio_files = session[const.AUDIO_FILES_KEY]
        for audio_file in session_audio_files:
            if audio_file[const.PATH_KEY] == audio_path:
                session_audio_files.remove(audio_file)
                break
        session[const.AUDIO_FILES_KEY] = session_audio_files
        sessions_dict[session_name] = session
    _update_sessions_json(sessions_dict)

if __name__ == '__main__':
    """
    For testing purposes.
    """
    default_sessions_json()
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
    delete_audio_file('test3', "test2.mp3")

    update_session_settings('test3', None, 5, None, 5)
    update_session_settings('test3', 10, 10, 10, 10)
    update_session_settings('test3', 5, None, 5, 10)
