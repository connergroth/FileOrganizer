import os
import sys
import time
import glob
import shutil
import logging
from os.path import splitext, exists, join
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "C:/Users/Conner Groth/Downloads"
dest_dir_image = "C:/Users/Conner Groth/Images" 
dest_dir_icon = "C:/Users/Conner Groth/Icons" 
dest_dir_document = "C:/Users/Conner Groth/Documents" 
dest_dir_text = "C:/Users/Conner Groth/Text" 
dest_dir_py = "C:/Users/Conner Groth/Python" 
dest_dir_song = "C:/Users/Conner Groth/Songs/LocalFiles 2" 
dest_dir_video = "C:/Users/Conner Groth/Videos" 


def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = makeUnique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        os.rename(oldName, newName)
    shutil.move(entry, dest)

class MoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            name = os.path.basename(event.src_path)

            if name.endswith('.tmp'):
                print(f"Skipping temp file: {name}")
                cleanup_temp_files()
                return

            dest = source_dir
            entry = event.src_path
            if name.endswith('.png') or name.endswith('.PNG') or name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.webp'):
                dest = dest_dir_image
            elif name.endswith('.svg'):
                dest = dest_dir_icon
            elif name.endswith('.pdf') or name.endswith('.tex'):
                dest = dest_dir_document
            elif name.endswith('.txt'):
                dest = dest_dir_text
            elif name.endswith('.py'):
                dest = dest_dir_py
            elif name.endswith('.wav') or name.endswith('.mp3') or name.endswith('.m4a'):
                if os.path.getsize(entry) < 25000000:
                    dest = dest_dir_song
                else:
                    dest = dest_dir_video  
    
            move(dest, entry, name)
            print(f"Moved: {name} to {dest}") 

def cleanup_temp_files():
    """ Delete .tmp files from Downloads """
    now = time.time()
    temp_files = glob.glob(os.path.join(source_dir, "*.tmp"))

    for tempfile in temp_files:
        try:
            if now - os.path.getctime(tempfile) > 10:
                os.remove(tempfile)
                print(f"Deleted temp file: {tempfile}")
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

