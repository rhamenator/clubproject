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
batch_size = 50

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

# Function to get genders from Genderize API in batch
def get_genders(names):
    try:
        response = requests.get(f"https://api.genderize.io", params={'name[]': names})
        if response.status_code == 200:
            data = response.json()
            return {item['name']: item['gender'] for item in data}
        else:
            print(f"Error: Received status code {response.status_code} from Genderize API")
            return {}
    except Exception as e:
        print(f"Exception occurred: {e}")
        return {}

def random_gender():
    return fake.random_element(elements=('Mann', 'Kvinne', ''))

# Generate fake data
def generate_data(num_records, batch_size=50):
    data = []
    names = [fake.first_name() for _ in range(num_records)]
    
    for i in range(0, num_records, batch_size):
        batch_names = names[i:i + batch_size]
        genders = get_genders(batch_names)
        
        for j, first_name in enumerate(batch_names, i + 1):
            last_name = fake.last_name()
            gender = genders.get(first_name, 'Ukjent')
            if gender == 'male':
                gender = 'Mann'
            elif gender == 'female':
                gender = 'Kvinne'
            else:
                gender = random_gender()  # Unknown gender - assign a random gender
            birthdate = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age).strftime('%d.%m.%Y')
            email = fake.email()
            phone = fake.phone_number()
            address = fake.street_address()
            postal_code = fake.postcode()
            city = fake.city()
            guardian_first_name, guardian_last_name = random_guardian_name()
            guardian_phone = fake.phone_number()

            data.append((
                j, first_name, last_name, gender, birthdate, email, phone, 
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
