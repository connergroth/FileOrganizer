# FileOrganizer
A simple Python project that automatically organizes files from a source directory into categorized destination directories based on their file types. It uses the watchdog library to monitor a folder and move files as they are created.

## Features
Automatically organizes files from the Downloads folder.  
Supports various file types:  
Images (.png, .jpg, .jpeg, .webp)  
Icons (.svg)  
Documents (.pdf, .tex)  
Text files (.txt)  
Python scripts (.py)  
Audio files (.mp3, .wav, .m4a) based on size:  
Files smaller than 25 MB go to the Songs folder.  
Larger files are moved to the Videos folder.  
Creates unique filenames if duplicates are found.  
