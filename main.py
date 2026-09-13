from picamzero import Camera
from flask import Flask, send_file, make_response
from pathlib import Path
from os import mkdir, listdir
import datetime
import re
import json
import RPi.GPIO as GPIO

pin=37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)
led_is_on = False

default_cam_settings = {
        "ExposureTime": 5000,
        "AnalogueGain": 0.5,
        "Brightness": 0.0,
        "Contrast": 1.0,
        "Saturation": 1.0,
        "Sharpness": 1.0,
    }

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

def get_cam_settings(conf_file: Path = Path("./cam_settings.json")) -> dict:
    if not conf_file.exists():
        conf_file.touch()
        with open(conf_file, 'w') as f:
            json.dump(default_cam_settings, f)

    with open(conf_file, 'r') as f:
        output = json.load(f)
        return output

@app.route("/lamp", methods=['GET'])
def switchLamp(mode: bool = led_is_on):
    global led_is_on
    GPIO.output(pin, GPIO.LOW if mode else GPIO.HIGH)
    led_is_on = not mode
    return make_response(str(led_is_on), 200)

@app.route("/capture", methods=['GET'])
def capture():
    cam = Camera()
    cam.pc2.set_controls(get_cam_settings())
    file_name = download_folder.joinpath(next_file_name())
    print(file_name)
    cam.take_photo(file_name)
    return send_file(file_name, mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0")