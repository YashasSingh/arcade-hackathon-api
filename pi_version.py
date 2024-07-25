import time
import requests
import configparser
from datetime import datetime, timedelta

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['API']['key']
SLACK_ID = config['User']['slack_id']
GOAL_NAME = config['Session']['goal_name']
SESSION_NAME_BASE = config['Session']['session_name_base']
MAX_SESSIONS = 10
BREAK_DURATION = 1800  # Break duration in seconds
ADDITIONAL_WAIT = 300  # 5 minutes in seconds

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_current_session():
    response = requests.get(f"https://hackhour.hackclub.com/api/session/{SLACK_ID}", headers=headers)
    if response.status_code == 200:
        return response.json().get('data')
    return None

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
    session_number = 3
    x = "false"
    while session_number <= MAX_SESSIONS:
        # Check if within break periods
        current_time = datetime.now().time()
        if (12 <= current_time.hour < 13) or (18 <= current_time.hour < 19) or (22 <= current_time.hour or current_time.hour < 7):
            wait_for_break_period()
        
        # Check for active session and wait if needed
        current_session = get_current_session()
        if current_session and not current_session.get("completed"):
            remaining_time = current_session['remaining'] * 60  # Convert minutes to seconds
            print(f"Session active, waiting for remaining time ({remaining_time} seconds) + 5 minutes.")
            time.sleep(remaining_time + ADDITIONAL_WAIT)
            x="true"
        if x == "false":
            # Start a new session
            start_session(session_number)
            session_number += 1
        
            # Wait for 1 hour and 3 minutes before the next session
            time.sleep(3600 + 180)






if __name__ == "__main__":
    run_sessions()
