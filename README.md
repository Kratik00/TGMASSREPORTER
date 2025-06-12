# TGREPORTER - Telegram Mass Reporter Tool

**Author(TELEGRAM):** [@LP_LUCIFER](https://github.com/KRATIK00)  
**Description:** A Telegram mass reporting tool using multiple session files built with Telethon.

---

## ðŸš€ How It Works

The script uses Telethon to automate reporting of a specific Telegram user/channel using multiple accounts (sessions). It takes command-line arguments to determine the action (add session or mass report), then performs the required task.

---

## ðŸ“¦ File Structure

```
TGREPORTER/
â”œâ”€â”€ reper.py            # Main script
â”œâ”€â”€ requirements.txt    # Python dependencies
â”œâ”€â”€ README.md           # Overview of the tool
â”œâ”€â”€ sessions/           # Folder where all Telegram sessions are stored
```

---

## ðŸ§  Line-by-Line Breakdown (reper.py)

### 1. ðŸ“¥ Importing Modules
```python
import asyncio
import argparse
import os
import sys
from telethon.sync import TelegramClient
from telethon import functions, types
from colorama import Fore, Style, init
```
- `asyncio`: Allows concurrent/asynchronous reporting.
- `argparse`: Parses command-line arguments.
- `os`, `sys`: File and environment handling.
- `telethon`: Telegram API interactions.
- `colorama`: Colored terminal output.

---

### 2. ðŸŽ¨ Banner Display Function
```python
def show_banner():
    ...
```
- Displays a large, colorful banner using `colorama` every time the script starts.

---

### 3. ðŸ§¾ Argument Parsing
```python
parser = argparse.ArgumentParser()
parser.add_argument("-an", "--add_number", type=str)
parser.add_argument("-t", "--target", type=str)
parser.add_argument("-r", "--repeat", type=int)
parser.add_argument("-m", "--mode", type=str)
args = parser.parse_args()
```
- `-an`: Add a new Telegram session using phone number.
- `-t`: Target username to report.
- `-r`: Number of reports.
- `-m`: Report reason/mode (e.g., spam, violence).

---

### 4. ðŸ” Add New Session
```python
if args.add_number:
    ...
```
- Starts a new session and saves it in `sessions/`.
- Useful to create multiple Telegram accounts for mass action.

---

### 5. âš™ï¸ Reporting Function
```python
async def report(cli, target, reason):
    ...
```
- Reports the target user using a specific session.
- Uses `functions.messages.ReportRequest`.

---

### 6. ðŸš¨ Main Async Execution
```python
async def main():
    ...
```
- Loads all session files.
- Launches parallel reporting tasks using `asyncio.gather()`.

---

### 7. ðŸ§¨ Script Entry Point
```python
if __name__ == "__main__":
    init(autoreset=True)
    show_banner()
    asyncio.run(main())
```
- Ensures banner and main function run only when the script is executed directly.
- Initializes colorama with auto-reset.

---

## ðŸ›  Usage

### Add Session
```bash
python3 reper.py -an +1234567890
```

### Report Target
```bash
python3 reper.py -t target_username -r 100 -m spam
```

---

## âš ï¸ Disclaimer

This tool is for educational purposes only. Misuse for spamming or harassment may lead to account bans or legal action. Use responsibly.

---
# TGREPORTER - Telegram Mass Reporter Tool

**Author:** [@LP_LUCIFER](https://github.com/LP-LUCIFER)  
**Description:** A Telegram mass reporting tool using multiple session files built with Telethon.

---

## ðŸš€ How It Works

The script uses Telethon to automate reporting of a specific Telegram user/channel using multiple accounts (sessions). It takes command-line arguments to determine the action (add session or mass report), then performs the required task.

---

## ðŸ“¦ File Structure

```
TGREPORTER/
â”œâ”€â”€ reper.py            # Main script
â”œâ”€â”€ requirements.txt    # Python dependencies
â”œâ”€â”€ README.md           # Overview of the tool
â”œâ”€â”€ sessions/           # Folder where all Telegram sessions are stored
```

---

## ðŸ§  Line-by-Line Breakdown (reper.py)

### 1. ðŸ“¥ Importing Modules
```python
import asyncio
import argparse
import os
import sys
from telethon.sync import TelegramClient
from telethon import functions, types
from colorama import Fore, Style, init
```
- `asyncio`: Allows concurrent/asynchronous reporting.
- `argparse`: Parses command-line arguments.
- `os`, `sys`: File and environment handling.
- `telethon`: Telegram API interactions.
- `colorama`: Colored terminal output.

---

### 2. ðŸŽ¨ Banner Display Function
```python
def show_banner():
    ...
```
- Displays a large, colorful banner using `colorama` every time the script starts.

---

### 3. ðŸ§¾ Argument Parsing
```python
parser = argparse.ArgumentParser()
parser.add_argument("-an", "--add_number", type=str)
parser.add_argument("-t", "--target", type=str)
parser.add_argument("-r", "--repeat", type=int)
parser.add_argument("-m", "--mode", type=str)
args = parser.parse_args()
```
- `-an`: Add a new Telegram session using phone number.
- `-t`: Target username to report.
- `-r`: Number of reports.
- `-m`: Report reason/mode (e.g., spam, violence).

---

### 4. ðŸ” Add New Session
```python
if args.add_number:
    ...
```
- Starts a new session and saves it in `sessions/`.
- Useful to create multiple Telegram accounts for mass action.

---

### 5. âš™ï¸ Reporting Function
```python
async def report(cli, target, reason):
    ...
```
- Reports the target user using a specific session.
- Uses `functions.messages.ReportRequest`.

---

### 6. ðŸš¨ Main Async Execution
```python
async def main():
    ...
```
- Loads all session files.
- Launches parallel reporting tasks using `asyncio.gather()`.

---

### 7. ðŸ§¨ Script Entry Point
```python
if __name__ == "__main__":
    init(autoreset=True)
    show_banner()
    asyncio.run(main())
```
- Ensures banner and main function run only when the script is executed directly.
- Initializes colorama with auto-reset.

---

## ðŸ›  Usage

### Add Session
```bash
python3 reper.py -an +1234567890
```

### Report Target
```bash
python3 reper.py -t target_username -r 100 -m spam
```

---

## âš ï¸ Disclaimer

This tool is for educational purposes only. Misuse for spamming or harassment may lead to account bans or legal action. Use responsibly.

---
