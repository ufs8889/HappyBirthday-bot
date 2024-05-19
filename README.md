# Happy Birthday Bot

 A Telegram bot written in Python that sends messages every day at the exact time of an employee's birthday.

## Features

 - Sends automated birthday messages to employees on their birthdays. 
 - Customizable time for sending birthday messages.
 - Easy to set up and use.

## Installation

 Clone the repository:
```bash
git clone https://github.com/ufs8889/Happy_Birthday_bot.git
```
Create a virtual environment:
```bash
python -m venv env
```
Activate the virtual environment:
```
.\env\Scripts\Activate.ps1
```
Install all required libraries:
```
pip install -r requirements.txt
```
## Usage

Navigate to the bot directory:
```bash
cd Happy_Birthday_bot/telegram_bot
```
Edit your bot's credentials in the TSHN_Happy_birthday.py file:

Set your Telegram Bot token:
```
TOKEN = 'YOUR_TOKEN'
```
Set your chat ID:
```
CHAT_ID = 'YOUR_CHAT_ID'
```
Configure the time to send birthday messages in the TSHN_Happy_birthday.py file:
```
target_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
```
Run the bot:
```
python TSHN_Happy_birthday.py
```
## Contributing

Contributions are welcome! Please feel free to submit a pull request.

License:

This project is licensed under the MIT License - see the LICENSE file for details.
