# Converts the videos to mp3 
import os 
import subprocess
import re

files = os.listdir("videos") 
for file in files: 
    match = re.search(r'\d+', file)
    tutorial_number = match.group() if match else "0"
    file_name = file.split(" ｜ ")[0]
    print( tutorial_number,  file_name)
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{tutorial_number}_{file_name}.mp3"])