import time
import requests
import configparser
from datetime import datetime

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['API']['key']
SLACK_ID = config['User']['slack_id']
GOAL_NAME = config['Session']['goal_name']
SESSION_NAME_BASE = config['Session']['session_name_base']
MAX_SESSIONS = int(config['Session']['max_sessions'])
BREAK_DURATION = int(config['Breaks']['break_duration'])  # Break duration in seconds

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

def wait_for_break_period():
    current_time = datetime.now().time()
    if (current_time.hour == 12 and current_time.minute < 60) or (current_time.hour == 18 and current_time.minute < 60):
        print(f"Break time! Waiting for {BREAK_DURATION / 60} minutes.")
        time.sleep(BREAK_DURATION)

def run_sessions():
    session_number = 1
    while session_number <= MAX_SESSIONS:
        current_time = datetime.now().time()
        
        # Check for the break period
        if (12 <= current_time.hour < 13) or (18 <= current_time.hour < 19):
            wait_for_break_period()

        # Start a new session
        start_session(session_number)
        session_number += 1
        
        # Wait for 1 hour and 3 minutes before the next session
        time.sleep(3600 + 180)

if __name__ == "__main__":
    run_sessions()
