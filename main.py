import time
import requests

API_KEY = "your_api_key_here"  # Replace with your API key
SLACK_ID = "your_slack_id_here"  # Replace with the Slack ID
GOAL_NAME = "Hack Hour (Arcade)"
SESSION_NAME_BASE = "blaha blah ahdsl"

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

