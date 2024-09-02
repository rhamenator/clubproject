# create_fake_data.py
from faker import Faker
import sqlite3
import csv
import requests
from datetime import datetime

# Initialize Faker with Norwegian locale
fake = Faker('no_NO')

# Number of records to generate
num_records = 200

# Age constraints
min_age = 14
max_age = 20

# Define the SQLite database and table name
db_name = 'club_tracking.db'
members_table_name = 'members'
sign_in_table_name = 'sign_in'

# Define the CSV file name
csv_file = 'members.csv'

# Define the field names
fieldnames = [
    'id', 'first_name', 'last_name', 'gender', 'birthdate', 'email', 'phone', 
    'address', 'postal_code', 'city', 'guardian_first_name', 'guardian_last_name', 'guardian_phone', 'timestamp'
]

# Function to get gender from Genderize API
def get_gender(name):
    response = requests.get(f"https://api.genderize.io?name={name}")
    if response.status_code == 200:
        data = response.json()
        return data.get('gender')
    return None

# Function to generate a random guardian name
def random_guardian_name():
    return fake.first_name(), fake.last_name()

# Create the SQLite database and table if it doesn't exist
def create_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {members_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gender TEXT,
            birthdate TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            city TEXT NOT NULL,
            guardian_first_name TEXT,
            guardian_last_name TEXT,
            guardian_phone TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {sign_in_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert a record into the SQLite database
def insert_record(data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(f'''
        INSERT INTO {members_table_name} (
            first_name, last_name, gender, birthdate, email, phone, 
            address, postal_code, city, guardian_first_name, guardian_last_name, guardian_phone, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data + (timestamp,))
    conn.commit()
    conn.close()

# Append a record to the CSV file
def append_to_csv(data):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow(dict(zip(fieldnames, [None] + list(data) + [timestamp])))

# Function to generate a random gender in Norwegian
def random_gender():
    return fake.random_element(elements=('Mann', 'Kvinne'))

# Generate fake data
def generate_data(num_records):
    data = []
    for i in range(1, num_records + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        # gender = get_gender(first_name)
        # if gender == 'male':
        #     gender = 'Mann'
        # elif gender == 'female':
        #     gender = 'Kvinne'
        # else:
        #     gender = ''  # Unknown gender
        
        gender = random_gender()
        birthdate = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age).strftime('%d.%m.%Y')
        email = fake.email()
        phone = fake.phone_number()
        address = fake.street_address()
        postal_code = fake.postcode()
        city = fake.city()
        guardian_first_name, guardian_last_name = random_guardian_name()
        guardian_phone = fake.phone_number()

        data.append((
            i, first_name, last_name, gender, birthdate, email, phone, 
            address, postal_code, city, guardian_first_name, guardian_last_name, guardian_phone
        ))
    return data

# Main function to create the database, generate data, and insert it into the database
def main():
    create_database()
    data = generate_data(num_records)
    for record in data:
        insert_record(record[1:])
        append_to_csv(record[1:])
    print(f"{num_records} records have been generated and inserted into the {members_table_name} table in the {db_name} database.")

if __name__ == '__main__':
    main()
