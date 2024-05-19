from datetime import datetime
import sqlite3

# Get today's date
today = datetime.now()
todays_date = today.strftime('%d.%m')

def convert_date_format(date_str):
    # Parse the date string in 'DD.MM.YY' format
    date_obj = datetime.strptime(date_str, '%d.%m.%y')
    # Correctly interpret the year
    year = date_obj.year
    if year > today.year:
        year -= 100

    # Format the date to 'DD.MM.YYYY'
    formatted_date = date_obj.replace(year=year).strftime('%d.%m.%Y')

    # Calculate the age
    birth_date = date_obj.replace(year=year)
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
    matching_records = []
    for record in get_date_from_database():
        day_month = record[4][:5]  # Slice the date string to extract day and month
        if day_month == todays_date:
            # Convert the record to a list and modify the date format and calculate age
            age, formatted_date = convert_date_format(record[4])
            formatted_record = list(record[1:4]) + [age, formatted_date]
            matching_records.append(formatted_record)
    
    return matching_records


