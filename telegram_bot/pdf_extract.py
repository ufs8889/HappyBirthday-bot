import pdfplumber
import re
import sqlite3

def extract_info_from_pdf(file_path):
    unwanted_texts = ["17 мая 2024 г. Страница", "из 15","декабрь", "ноябрь","октябрь","сентябрь","август","июль","июнь","май","апрель","март","февраль","январь","Дни рождения сотрудников ГУП","Фамилия Имя Отчество", "Подразделение", "Должность", "Год", "рож."]

    def is_unwanted_line(line):
        return any(unwanted_text in line for unwanted_text in unwanted_texts)

    def format_line(line):
        # Regular expression to match the expected pattern
        match = re.match(r"^([\w\sЁёА-яёЁ]+) ([\w\.\d№-]+) ([\w\.-]+) (\d{2}\.\d{2}\.\d{2})$", line)
        if match:
            return [match.group(1), match.group(2), match.group(3), match.group(4)]
        else:
            # Try to infer the structure if the line doesn't match exactly
            parts = line.split()
            if len(parts) >= 4:
                name = " ".join(parts[:-3])
                subdivision = parts[-3]
                position = parts[-2]
                date = parts[-1]
                return [name, subdivision, position, date]
            return None

    extracted_data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                lines = page_text.split("\n")
                filtered_lines = [line for line in lines if not is_unwanted_line(line)]
                for line in filtered_lines:
                    formatted_line = format_line(line)
                    if formatted_line:
                        extracted_data.append(formatted_line)

    return extracted_data

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS birthdays (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    subdivision TEXT NOT NULL,
                    position TEXT NOT NULL,
                    date TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def insert_data(db_name, data):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.executemany('INSERT INTO birthdays (name, subdivision, position, date) VALUES (?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

# File path to your PDF
file_path = r'C:\Users\user\Desktop\telegram_bot\День рождения ГУП.pdf'
# Extract information from the PDF
extracted_data = extract_info_from_pdf(file_path)

# Database file
db_name = 'birthdays.db'
# Create the database and table
create_database(db_name)
# Insert data into the database
insert_data(db_name, extracted_data)

# Print the extracted data to verify
for record in extracted_data:
    print(record)
