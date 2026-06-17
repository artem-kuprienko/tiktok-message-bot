# TikTok Message Bot

Automated TikTok message sending on schedule. Bot launches browser, finds the contact, and sends a random message from your list once per day at a specified time.

## Features

- Scheduled sending (configurable time)
- Random message selection from list
- Automatic retry on failures
- Error logging

## Requirements

- Python 3.8+
- Chromium (installed via Playwright)
- Active TikTok session (initial login required)

## Installation

1. Clone repository:

git clone https://github.com/artem-kuprienko/tiktok-message-bot.git
cd tiktok-message-bot

2. Create virtual environment (recommended):

python -m venv venv

Windows:
venv\\Scripts\\activate

Linux/Mac:
source venv/bin/activate

3. Install dependencies:

pip install -r requirements.txt
playwright install chromium

4. Configure environment:

cp .env.example .env

Open .env and fill in your data (read .env.example for explanation):

HEADLESS=false
FRIEND_NAME=ContactName
MESSAGES=Hello!|Auto-Message
CHECK_INTERVAL_SEC=600
SEND_TIME_HOUR=9

open .env and make HEADLESS false (if not did before)

5. First run (TikTok login):

python main.py

On first run:
- Browser will open
- Log into your TikTok account
- Navigate to Messages
- Session will be saved automatically to session_data_tiktok folder
- Stop the script (Ctrl+C)

6. Enable headless mode:

In .env change:
HEADLESS=true

7. Run the bot:

python main.py

## Configuration

All settings are configured in .env file also there file named ".env.example":

HEADLESS - Headless browser mode (true/false)
FRIEND_NAME - Exact contact name from TikTok
MESSAGES - Message variants separated by |
CHECK_INTERVAL_SEC - Check interval in seconds
SEND_TIME_HOUR - Send hour (0-23, local time)

### Examples

Single message:
MESSAGES=Good morning!

Random selection from multiple:
MESSAGES=Hello!|How are you?|Good morning!

