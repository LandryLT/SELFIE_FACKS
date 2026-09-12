from picamzero import Camera
from flask import Flask, send_file
from pathlib import Path
from os import mkdir, listdir
import datetime
import re

app = Flask(__name__)
cam = Camera()
download_folder = Path('./reel')
if not download_folder.exists():
    mkdir(download_folder)

def next_file_name() -> str:
    all_files = listdir(download_folder)
    max_index = 0
    for file in all_files:
        curr_ind = int(re.search(r'^\d\d\d\d\d\d', file))
        max_index = max(curr_ind, max_index)
    return str(max_index).zfill(6) + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + "_facks_watcher.jpg"

@app.route("/capture", methods=['GET'])
def capture():
    file_name = next_file_name()
    print(file_name)
    cam.capture(file_name)
    send_file(file_name, mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0")