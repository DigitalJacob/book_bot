# 📖 Book Bot

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-green.svg)](https://docs.aiogram.dev/)
[![aiofiles](https://img.shields.io/badge/aiofiles-24.x-red.svg)](https://github.com/Tinche/aiofiles)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Telegram bot for reading books with bookmark support, page-by-page navigation, and persistent storage.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.12+** | Core programming language |
| **aiogram 3.x** | Telegram Bot API framework |
| **aiofiles** | Asynchronous file operations for JSON storage |
| **environs** | Environment variables management |
| **aiohttp-socks** | Proxy support (HTTP/HTTPS/SOCKS5) |

## Features

- 📚 Read books page by page directly in Telegram
- 🔖 Add and remove bookmarks for quick navigation
- 📱 Inline keyboards for intuitive controls
- 💾 Persistent storage with JSON + aiofiles (no database setup required)
- 🔌 Proxy support for restricted networks
- 📝 Configurable logging with automatic rotation
- ⚡ Fully asynchronous — never blocks your bot

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/help` | Display help information |
| `/beginning` | Jump to the first page of the book |
| `/continue` | Resume reading from your last page |
| `/bookmarks` | View and manage your bookmarks |

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:akovveretin/book_bot.git
cd book_bot
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```
Edit .env and add your bot token:

BOT_TOKEN=your_telegram_bot_token_here
LOG_LEVEL=your_log_level #DEBUG for development, INFO for production

Get your token from @BotFather.

### 5. Add a book

Place your .txt book file in the book/ directory:

```bash
book/
└── your_book.txt
```

### 6. Run the bot

```bash
python main.py
```

You should see:

Bot configured and starting

## Project Structure

```bash
book_bot/
├── book/                      # Book text files
├── config/                    # Configuration management
├── database/                  # JSON database with aiofiles
├── filters/                   # Custom callback filters
├── handlers/                  # Message and callback handlers
├── keyboards/                 # Inline keyboards
├── lexicon/                   # Text messages
├── log_config/                # Logging configuration with rotation
├── services/                  # Business logic layer
├── .env.example               # Environment variables template
├── main.py                    # Entry point
└── requirements.txt           # Dependencies
```

## Navigation

When reading a book, the bot shows three inline buttons:

When reading a book, the bot shows three inline buttons:

| Button | Action                                                        |
|--------|---------------------------------------------------------------|
| `<<` | Go to previous page                                           |
| `5/100` | Current page indicator (click this button to add current page to bookmarks) |
| `>>` | Go to next page                                               |

## Proxy Support

Configure proxy in .env.
To disable proxy, comment out or remove all PROXY_* lines.

## Logging

Logs are written to bot.log with automatic rotation.

## Database

User data is stored in db.json. No external database setup required. 
The database is saved automatically after every change.

## License

MIT License — free to use, modify, and distribute.