# Listen Up! Audio Trivia - Magnet Forensics Hackathon
### By Ari Rubin, Emily Tang, Kaylee Nasser, and Raven Sim

Build an application that takes a folder of audio files (or other source) and plays a random file at a random timestamp for a specified interval and allows you to guess the name of the file (or other success criteria).

Could be used for guessing music, my encyclopedic knowledge of Avatar the Last Airbender episodes, or even language learning: import foreign media files and use it for listening practice!

Bonus points if we could import subtitle tracks and display the subtitle of that timestamp as part of the answer.

# Description
*Build an application that takes a folder of audio files (or other source) and plays a random file at a random timestamp for a specified interval and allows you to guess the name of the file (or other success criteria).  
Could be used for guessing music, my encyclopedic knowledge of Avatar the Last Airbender episodes, or even language learning: import foreign media files and use it for listening practice!  
Bonus points if we could import subtitle tracks and display the subtitle of that timestamp as part of the answer.*


- Want to work directly with files
	- probably easier/better to work with references to files stored locally rather than doing any copying
- we need user settings to be stored, if we do Slackbot, does that require some db work? because we'd be keeping users separate on the backend 

- Emily: importing from local -> associating to a certain session? 
	- import folder and individual files?
		- files for now
		- every session has a `sessionName.json` that holds a list of filepaths for the tracks
```
{
	"sessionname": "value"
}
	"audiopaths":[
	"path/tofile",
	"other/path"
	]
}
```

- assume you're given a list/array of filepaths (frontend will get this for you)
- settings.py -> probs just json/functions #ari
- tracks.py -> class #kaylee
- sessions.py -> probs a class 
	- json for import #emily
- frontend.py -> tkinter #raven
- utilities.py -> common functions 

- playing files from a certain spot
	- audiofile class?
		- - props
		- filename, session, duration, 
- user settings stored locally -> importing/saving
	- given a settings page exists, how are we storing a user's settings?
		- json file
		- 
- Raven: frontend -> hello world tkinter -> making some pages
- success criteria/points
	- some basic functions for tracking score

- classes -> audio files (tracks)
	- props
		- filename, session, duration, 

- class -> session
	- a collection of tracks for a single session
	- 


# ❓ Questions ❓
- What is the scope of the project? What would we like to have completed by the demo?
	- upload 2+ audio files (mp3 to start, mp4 also would be cool)
		- youtube links as input as well
			- download audio/video(?) from youtube and store locally
				- default to title name, allow option to change
		- presets? and options to add
	- upload audio to different groups/sessions
	- press a button to play a random audio file at a random timestamp for a specified interval
	- have the ability to change the interval length
	- have the ability to set start/end bounds to account for things like end credits/theme songs
	- have the ability to switch between "sessions"/groups of audio files
	- 
- Team preferences/experience?
	- frontend/backend, have you worked with audio, etc
	- anything you'd hate doing?
		- Emily -> no frontend lol
	- anything in particular you want to learn? 
		- Kaylee -> nice to do some real coding pls
			- frontend or backend (prefer back)
			- did yt to audio in python before -> does library still exist?
		- Ari -> no preference
	- hours/availability? How often are we checking in?
		- 9-5
- Tech stack
		- what language/libraries are we using?
			- standalone desktop app
			**- python? easy, intuitive, I have a bit of Tkinter experience for frontend**
				- .NET? there's Maui for frontend that looks pretty straightforward
					- makes it more applicable to magnet, so we could work with audio files in a more interesting way
					- unity?
			- Slackbot/js? 
				- ppl could test it 
				- could run into some barriers with getting the audio + user management
- Research/rabbit hole: how the heck to subtitle tracks work? if they're embedded into certain filetypes, 

# Pages
## Main
- **button**: upload files
- **button**: open an existing "session"
## Session
- **button**: play
	- plays a random audio at a random timestamp following the settings
- **slider**/settings: interval
- **button**: +5s 
	- to be used after the initial audio is played, to allow an additional X seconds to play
- **button**: replay
	- replays the entire duration of the audio played so far from the beginning
		- so if they pressed +5s, and the original interval was 3s, then pressing replay would play the whole 8s over again
- **button**: show answer
	- reveals the filename, or the subtitles if available:
		- auto captions?
			- whisper.ai?
- **button**: check/x for success/fail
	- extra: or multiple choice option?
## Settings
- slider/settings: default interval
	- how long each audio initially plays for
- slider/settings: start/end buffer
	- if applicable, tracks will skip the first/last X seconds
		- if the remaining audio is shorter than a certain threshold, ignore this
- list/button: manage session audio
	- interface for adding/removing audio from a specific session?
- setting: change path to downloads

# Other Thoughts
- probably just store a `settings.json` for main settings, and have different `session_name.json` for settings of individual sessions + references to the files/folders
- should set up a git at some point (can someone else do this i dont wanna :sob:)
## Getting your development environment set up

The first step is to pull the code from this remote repository onto your computer:

```bash
git clone git@github.com:kayleenasser/audio-trivia.git
```

You may notice that this will create a folder on your computer called `audio-trivia`. `cd` into this newly created folder.

### Create a new branch for the ticket

If you want to start working on a new part of the product, you first need to create a new branch so you don't change any of the `main` code once you push to the remote repo!!

- First, make sure you pull from `main`, since that is what you'll eventually be merging your code into (and we want the most up-to-date info).

```bash
git switch main
git pull
```

- Then, make a new branch and automatically switch to it with:

```bash
git checkout -b yourname
```

where `yourname` is your name (lol). 

### Pushing your changes

Once you've finished a commit, push it to the remote repo on your new branch:

```
git add <list of files separated by spaces, or . for all files>
git commit -m "A descriptive commit message"
git push 
```

### Reviewing a pull request

If you encounter any bugs, errors, warnings, improper formatting or typos, or simply something that you believe isn't written in the best way, submit a review on the PR explaining your concern. When you submit a review on a PR, you can either accept it, request changes, or simply comment on something without doing either. We don't want to accept any code into `main` until all concerns from all team members are resolved.

When comments are left on PRs, it means that not everyone is satisfied with the code that is being proposed. This will generate a discussion from possibly multiple team members, hopefully including the initiator of the PR. A comment thread can be "resolved" either through a discussion ending in a consensus decision that the concern is unfounded, or additional commits to the PR which fix the concern (you can still commit to a branch and therefore a PR after it has been opened), in which case additional comments should be made referencing these commits and explaining how they resolve the concern.

Once all of the concerns have been resolved, and the PR has received two approvals from members of the team, it will be merged into `main`. Congratulations!
