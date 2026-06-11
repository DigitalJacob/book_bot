# 📖 Book Bot

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-green.svg)](https://docs.aiogram.dev/)
[![aiofiles](https://img.shields.io/badge/aiofiles-24.x-red.svg)](https://github.com/Tinche/aiofiles)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Telegram bot for reading books: pick from a library, flip through pages, bookmark passages, and pick up where you left off — with separate progress tracked for each title.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.12+** | Core language |
| **aiogram 3.x** | Telegram Bot API framework |
| **aiofiles** | Async read/write for `db.json` |
| **environs** | Environment variable management |
| **aiohttp-socks** | Proxy support (HTTP/HTTPS/SOCKS5) |

## Features

- 📚 **Multi-book library** — users choose a title via `/books`
- 📖 **Page-by-page reading** directly in Telegram
- 🔖 **Bookmarks** with quick navigation and editing
- 💾 **Per-book progress** stored in `db.json` (page + bookmarks)
- 🔌 **Proxy support** for restricted networks
- 📝 **Rotating logs** written to `bot.log`
- ⚡ **Fully asynchronous** — the bot never blocks on I/O

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/books` | Choose a book from the library |
| `/beginning` | Jump to the first page of the current book |
| `/continue` | Resume from the saved page |
| `/bookmarks` | View bookmarks for the current book |
| `/help` | Help and command list |

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:DigitalJacob/book_bot.git
cd book_bot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Add your bot token to `.env` (get one from [@BotFather](https://t.me/BotFather)):

```env
BOT_TOKEN=your_telegram_bot_token_here
LOG_LEVEL=INFO
```

Use `LOG_LEVEL=DEBUG` during development.

### 5. Add books

Place `.txt` files in the `books/` directory (see [The `books/` directory](#the-books-directory) below).

### 6. Run the bot

```bash
python main.py
```

You should see this in the log:

```
Bot configured and starting
```

## The `books/` directory

Each book is a single plain-text file encoded in **UTF-8**.

Current library:

```
books/
├── Ангелы_и_демоны.txt
├── Заводной_апельсин.txt
└── По_осколкам_твоего_сердца.txt
```

**The filename without `.txt` is the book ID** used in the bot and in `db.json`.  
**Underscores** in filenames are shown as spaces in the menu — for example,  
`Заводной_апельсин.txt` appears as **Заводной апельсин**.

### Cyrillic and non-ASCII filenames

Yes, they work fine. Python, UTF-8 file I/O, and macOS/Linux filesystems all handle them without issue.

One constraint: Telegram limits inline button `callback_data` to **64 bytes**. The bot uses the prefix `book:` (5 bytes), leaving the rest for the filename. Typical Cyrillic titles fit comfortably. If a name is too long, the bot logs a warning on startup — shorten the filename.

Naming guidelines:

- Latin or Cyrillic characters are both fine
- Use `_` between words; avoid spaces in filenames
- Avoid special characters: `/ \ : * ? " < > |`

## Adding a new book

1. Save the book text as a `.txt` file in **UTF-8**.
2. Name the file using underscores instead of spaces, e.g. `War_and_Peace.txt`.
3. Copy it into `books/`:
   ```bash
   cp ~/Downloads/War_and_Peace.txt books/
   ```
4. Restart the bot:
   ```bash
   python main.py
   ```
5. Check the log for a line like `Загружена книга: ...` (book loaded).
6. Open `/books` in Telegram — the new title should appear in the list.

No code changes are required. `BookManager` scans `books/` on every startup.

**User progress** for the new title is created automatically the first time someone selects it. Existing entries in `db.json` for other books are left untouched.

## Project structure

```
book_bot/
├── books/                     # Book text files (.txt, UTF-8)
├── config/                    # Configuration from .env
├── database/                  # db.json load/save logic
├── filters/                   # Custom callback filters
├── handlers/                  # Command and callback handlers
├── keyboards/                 # Inline keyboards
├── lexicon/                   # Bot message texts
├── log_config/                # Logging setup
├── services/                  # BookManager, file parsing, user helpers
├── db.json                    # Reader progress (auto-created)
├── .env.example
├── main.py
└── requirements.txt
```

## Reading navigation

While reading, the bot shows three inline buttons:

| Button | Action |
|--------|--------|
| `<<` | Previous page |
| `5/100` | Current page (tap to bookmark) |
| `>>` | Next page |

## Database

All user data is stored in `db.json`. No external database setup is required.

Example user record:

```json
{
  "current_book": "Заводной_апельсин",
  "books": {
    "Заводной_апельсин": {
      "current_page": 42,
      "bookmarks": [10, 25]
    },
    "Ангелы_и_демоны": {
      "current_page": 1,
      "bookmarks": []
    }
  }
}
```

The file is saved automatically after bookmarks change, pages are turned, or a book is selected.

## Proxy support

Configure proxy settings in `.env`. To disable the proxy, remove or comment out all `PROXY_*` variables.

## Logging

Logs are written to `bot.log` with automatic rotation.

## License

MIT License — free to use, modify, and distribute.
