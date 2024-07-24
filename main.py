import time
import requests
import configparser

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['API']['key']
SLACK_ID = config['User']['slack_id']
GOAL_NAME = config['Session']['goal_name']
SESSION_NAME_BASE = config['Session']['session_name_base']

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

def run_sessions():
    session_number = 1
    while True:
        start_session(session_number)
        session_number += 1
        # Wait for 1 hour and 3 minutes
        time.sleep(3600 + 180)  # 3600 seconds in an hour + 180 seconds (3 minutes)

if __name__ == "__main__":
    run_sessions()
