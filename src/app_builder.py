# Name: 		app_builder.py
# Author:		Raven Sim
# Date: 		Oct 5th, 2023
# Contributors: 
# Purpose:		To export the Listen Up! software as a standalone Executable.

import PyInstaller.__main__
import sys 
from os import path 
site_packages = next(p for p in sys.path if 'site-packages' in p) 
pptx_file = path.join(site_packages,"pptx\\templates;pptx\\templates")

PyInstaller.__main__.run([
	'frontend.py',			# main script to package
	'--onefile', 					# single file executable
	'--name',
	'Listen Up!',		# name of executable file
	'--icon',
	'assets/icon.ico',	# image file to use for the executable icon
	#'--windowed',			# hide the console when running the executable #comment out if you need to debug while running from executable
	'--add-data',
	'assets/icon.ico;.',		# import the icon file as a resource to be used (for the taskbar/tkinter window icon)
    '--add-data',
	'assets/dark-bg.png;.',
    '--add-data',
	'assets/banner.PNG;.',
    '--add-data',
	'sessions.json;.'
    
])