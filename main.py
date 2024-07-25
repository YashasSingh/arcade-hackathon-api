import time
import requests
import configparser
import shutil
import os
from datetime import datetime, timedelta

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['API']['key']
SLACK_ID = config['User']['slack_id']
GOAL_NAME = config['Session']['goal_name']
SESSION_NAME_BASE = config['Session']['session_name_base']
MAX_SESSIONS = int(config['Session']['max_sessions'])
BREAK_DURATION = int(config['Breaks']['break_duration'])  # 30 minutes in seconds
FOLDER_TO_COPY = "path/to/folder"  # Folder to be copied
DESTINATION_BASE = "path/to/destination/folder"  # Base destination folder

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def start_session(session_number):
    session_name = f"{SESSION_NAME_BASE} {session_number}"
    data = {
        "work": session_name
    }
    response = requests.post(f"https://hackhour.hackclub.com/api/start/{SLACK_ID}", json=data, headers=headers)
    if response.status_code == 200 and response.json().get("ok"):
        print(f"Started session: {session_name}")
    else:
        print(f"Failed to start session: {session_name}", response.text)

def copy_folder(session_number):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    destination = os.path.join(DESTINATION_BASE, f"session_{session_number}_{timestamp}")
    shutil.copytree(FOLDER_TO_COPY, destination)
    print(f"Copied folder to {destination}")

def wait_for_break_period():
    current_time = datetime.now().time()
    if (12 <= current_time.hour < 13) or (18 <= current_time.hour < 19):
        print(f"Taking a meal break at {current_time}. Waiting for {BREAK_DURATION / 60} minutes.")
        time.sleep(BREAK_DURATION)
    elif (22 <= current_time.hour or current_time.hour < 7):
        print(f"Sleeping break. Current time: {current_time}.")
        sleep_end = datetime.combine(datetime.today(), datetime.time(7, 0, 0))
        if current_time.hour >= 22:
            sleep_end = sleep_end + timedelta(days=1)  # Adjust to next day if it's currently past 10 PM
        sleep_duration = (sleep_end - datetime.now()).total_seconds()
        time.sleep(sleep_duration)

def run_sessions():
    session_number = 1
    while session_number <= MAX_SESSIONS:
        current_time = datetime.now().time()
        
        # Check if within break periods
        if (12 <= current_time.hour < 13) or (18 <= current_time.hour < 19) or (22 <= current_time.hour or current_time.hour < 7):
            wait_for_break_period()
        
        # Start a new session
        start_session(session_number)
        
        # Copy the folder after session starts
        copy_folder(session_number)

        session_number += 1
        
        # Wait for 1 hour and 3 minutes before the next session
        time.sleep(3600 + 180)

if __name__ == "__main__":
    run_sessions()
