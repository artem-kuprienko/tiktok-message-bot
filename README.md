# TikTok Message Bot

Automated TikTok message sending on schedule. Bot launches browser, finds the contact, and sends a random message from your list once per day at a specified time.

## Features

- 🕐 Scheduled sending (configurable time)
- 🎲 Random message selection from list
- 🔄 Automatic retry on failures
- 📝 Error logging

## Requirements

- Python 3.8+
- Chromium (installed via Playwright)
- Active TikTok session (initial login required)

## Installation

### 1. Clone repository

```bash
git clone https://github.com/artem-kuprienko/tiktok-message-bot.git
cd tiktok-message-bot
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Configure environment

```bash
cp .env.example .env
```

Open `.env` file and fill in your data:

```env
HEADLESS=false
FRIEND_NAME=ContactName
MESSAGES=Hello!|Auto-Message
CHECK_INTERVAL_SEC=600
SEND_TIME_HOUR=9
```

> See `.env.example` for detailed explanation of each parameter

### 5. First run (TikTok login)

```bash
python main.py
```

On first run:
- Browser window will open
- Log into your TikTok account
- Navigate to Messages page
- Session will be saved automatically to `session_data_tiktok/` folder
- As you logged in stop the script with `Ctrl+C`

### 6. Enable headless mode

Edit `.env` file:

```env
HEADLESS=true
```

### 7. Run the bot

```bash
python main.py
```

## Configuration

All settings are in `.env` file:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `HEADLESS` | Browser visibility (`true` = hidden, `false` = visible) | `true` |
| `FRIEND_NAME` | Exact contact name from TikTok messages | `JohnDoe` |
| `MESSAGES` | Messages separated by `\|` for random selection | `Hi!\|Hello!` |
| `CHECK_INTERVAL_SEC` | How often to check time (in seconds) | `600` |
| `SEND_TIME_HOUR` | Hour to send message (0-23, local time) | `9` |

### Configuration Examples

**Single message:**
```env
MESSAGES=Good morning!
```

**Random selection from multiple:**
```env
MESSAGES=Hello!|How are you?|Good morning!|👋
```

**Send at 8:00 AM with 5-minute checks:**
```env
SEND_TIME_HOUR=8
CHECK_INTERVAL_SEC=300
```

## How It Works

1. Bot checks current time every `CHECK_INTERVAL_SEC` seconds
2. If time ≥ `SEND_TIME_HOUR` and message not sent today:
   - Launches browser
   - Finds contact by `FRIEND_NAME`
   - Picks random message from `MESSAGES`
   - Sends message
   - Records date in `timer.txt`
3. If sending fails, retries on next check

## Logs

- **`error_log.txt`** - All errors with timestamps
- **`timer.txt`** - Dates of successful sends
- **Console** - Real-time status updates

## Troubleshooting

### Bot cannot find contact

Check exact spelling. Run with `HEADLESS=false` to see contact list.

### Session expires

TikTok may reset sessions periodically. Re-login:
1. Set `HEADLESS=false` in `.env`
2. Run `python main.py`
3. Login again
4. Set `HEADLESS=true`

### Browser fails to launch

Install Chromium:
```bash
playwright install chromium
```


## Disclaimer

This bot uses browser automation and may violate TikTok's Terms of Service. Use at your own risk. Author is not responsible for account bans or other consequences. for informational purposes only..

## Support

- 🐛 Found a bug? [Create an issue](https://github.com/artem-kuprienko/tiktok-message-bot/issues)
