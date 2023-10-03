# Audio Trivia
## Magnet Forensics Hackathon
### By Ari Rubin, Emily Tang, Kaylee Nasser, and Raven Sim

Build an application that takes a folder of audio files (or other source) and plays a random file at a random timestamp for a specified interval and allows you to guess the name of the file (or other success criteria).

Could be used for guessing music, my encyclopedic knowledge of Avatar the Last Airbender episodes, or even language learning: import foreign media files and use it for listening practice!

Bonus points if we could import subtitle tracks and display the subtitle of that timestamp as part of the answer.

## Getting your development environment set up

The first step is to pull the code from this remote repository onto your computer:

```bash
git clone git@github.com:kayleenasser/audio-trivia.git
```

You may notice that this will create a folder on your computer called `audio-trivia`. `cd` into this newly created folder.

### Create a new branch for the ticket

If you want to start working on a new part of the product, you first need to create a new branch so you don't change any of the `main` code once you push to the remote repo!!

- First, make sure you pull from `main`, since that is what you'll eventually be merging your code into (and we want the most up-to-date info).

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
