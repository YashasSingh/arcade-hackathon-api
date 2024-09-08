


# Session Manager for Hack Hour
![IMG_3618](https://github.com/user-attachments/assets/9fc7f93e-4ddb-4e6d-b03f-b3cfebea8ad9)



This Python script automates session management for Hack Club's Hack Hour project tracker. It checks for active sessions, manages break periods, and starts new sessions at regular intervals, with configurable parameters stored in an `.ini` file.

## Features

- **Session Management:** Automatically starts a new session after a configurable delay.
- **Active Session Check:** Verifies if a session is already in progress before starting a new one, waits for the existing session to finish plus an additional 5 minutes.
- **Break Periods:** Incorporates scheduled breaks:
  - **Lunch Break:** 12:00 PM to 12:59 PM.
  - **Dinner Break:** 6:00 PM to 6:59 PM.
  - **Sleep Break:** 10:00 PM to 6:59 AM.
- **Configurable Parameters:** All key parameters (API key, Slack ID, session names, break times, etc.) are stored in a `config.ini` file.

## Requirements

- Python 3.x
- `requests` library

Install the `requests` library using pip if you haven't already:

```bash
pip install requests
```

## Configuration

Create a `config.ini` file in the same directory as your script with the following structure:

```ini
[API]
key = your_api_key_here

[User]
slack_id = your_slack_id_here

[Session]
goal_name = Hack Hour (Arcade)
session_name_base = blaha blah ahdsl
max_sessions = 10

[Breaks]
break_duration = 1800  # 30 minutes in seconds
```

- `key`: Your API key for the Hack Hour API.
- `slack_id`: Your Slack ID used in Hack Hour.
- `goal_name`: The name of the goal for tracking purposes.
- `session_name_base`: The base name for each session. Session names will be suffixed with a number (e.g., `blaha blah ahdsl 1`).
- `max_sessions`: The total number of sessions to run.
- `break_duration`: The duration of breaks in seconds (e.g., 1800 seconds for 30 minutes).

## How It Works

1. **Starting Sessions**: The script starts a new session with the specified base name and a session number (e.g., `blaha blah ahdsl 1`).
2. **Checking Active Sessions**: Before starting a new session, the script checks if there is already an active session. If one is active, it waits for the remaining time of that session plus an additional 5 minutes.
3. **Break Management**: The script pauses during defined break periods:
   - Lunch: 12:00 PM - 12:59 PM
   - Dinner: 6:00 PM - 6:59 PM
   - Sleep: 10:00 PM - 6:59 AM
4. **Looping Sessions**: The script repeats this process for the number of sessions specified in the `max_sessions` parameter.

## Running the Script

To run the script, simply execute it with Python:

```bash
python session_manager.py
```

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.

## Disclaimer

Please note that the reliability of the Hack Hour API is not guaranteed. Data loss may occur, and there's no guarantee that your sessions will be registered accurately. Use at your own risk.

## Contributions

Contributions are welcome! If you find a bug or have a suggestion for improvement, feel free to open an issue or submit a pull request.




