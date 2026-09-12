from picamzero import Camera
from flask import Flask, send_file
from pathlib import Path
from os import mkdir, listdir
import datetime
import re

download_folder = Path('./reel')
if not download_folder.exists():
    mkdir(download_folder)
app = Flask(__name__)

def next_file_name() -> str:
    all_files = listdir(download_folder)
    max_index = 0
    for file in all_files:        
        file_prefix = re.match(r'^\d\d\d\d\d\d', file)
        curr_ind = int(file_prefix.group(0) if file_prefix else 0)
        max_index = max(curr_ind + 1, max_index)
    return str(max_index).zfill(6) + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + "_facks_watcher.jpg"

@app.route("/capture", methods=['GET'])
def capture():
    cam = Camera()
    file_name = download_folder.joinpath(next_file_name())
    print(file_name)
    cam.take_photo(file_name)
    return send_file(file_name, mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0")