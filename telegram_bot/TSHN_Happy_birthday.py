import logging
from datetime import datetime, timedelta
from pytz import timezone
from telegram import Bot
from telegram.ext import Updater, CallbackContext
import sqlite3

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your bot's token
TOKEN = 'JHHKHKHKHJGJ'
CHAT_ID = '4646'

# Time zone for GMT+5
tz = timezone('Etc/GMT-5')

def convert_date_format(date_str):
    # Parse the date string in 'DD.MM.YY' format
    date_obj = datetime.strptime(date_str, '%d.%m.%y')
    year = date_obj.year
    if year > datetime.now().year:
        year -= 100

    # Format the date to 'DD.MM.YYYY'
    formatted_date = date_obj.replace(year=year).strftime('%d.%m.%Y')

    # Calculate the age
    birth_date = date_obj.replace(year=year)
    today = datetime.now()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return [age, formatted_date]

def get_date_from_database():
    conn = sqlite3.connect('birthdays.db')
    c = conn.cursor()
    c.execute("SELECT * FROM birthdays")
    date_row = c.fetchall()
    conn.close()
    return date_row if date_row else []

def run_every_day():
    todays_date = datetime.now().strftime('%d.%m')
    matching_records = []
    for record in get_date_from_database():
        day_month = record[4][:5]
        if day_month == todays_date:
            age, formatted_date = convert_date_format(record[4])
            formatted_record = list(record[1:4]) + [age, formatted_date]
            matching_records.append(formatted_record)
    
    return matching_records

def format_message(records):
    if not records:
        return "No birthdays today."

    # Header for the message
    message = "Today's Birthdays🎂🎉!\n\n"

    for record in records:
        # Formatting each record
        formatted_record = (
            f"{record[0]}\n"
            f"Works in: {record[1]}\n"
            f"Works as: {record[2]}\n"
            f"Aged: {record[3]}\n"
            f"Birthday: {record[4]}\n\n"
        )
        message += formatted_record

    return message

def send_message(context: CallbackContext):
    bot = context.bot
    records = run_every_day()
    message = format_message(records)
    bot.send_message(chat_id=CHAT_ID, text=message)

def schedule_message(updater: Updater):
    now = datetime.now(tz)
    target_time = now.replace(hour=13, minute=43, second=0, microsecond=0)

    if now > target_time:
        target_time += timedelta(days=1)
    
    delta = (target_time - now).total_seconds()
    
    updater.job_queue.run_once(send_message, when=delta)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_error_handler(lambda update, context: logger.error(context.error))

    updater.start_polling()
    logger.info("Bot started")

    schedule_message(updater)

    updater.idle()

if __name__ == '__main__':
    main()
