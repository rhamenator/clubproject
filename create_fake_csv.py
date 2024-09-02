# create_fake_csv.py
from faker import Faker
import csv

# Initialize Faker with Norwegian locale
fake = Faker('no_NO')

# Number of records to generate
num_records = 200

# Age constraints
min_age = 14
max_age = 20

# Define the CSV file name
csv_file = 'norwegian_data.csv'

# Define the field names
fieldnames = [
    'id', 'first_name', 'last_name', 'gender', 'birthdate', 'email', 'phone', 
    'address', 'postal_code', 'city', 'guardian_first_name', 'guardian_last_name', 'guardian_phone', 'timestamp'
]

# Function to generate a random gender
def random_gender():
    return fake.random_element(elements=('Male', 'Female', 'Non-binary', 'Genderqueer', 'Agender', 'Other'))

# Function to generate a random guardian name
def random_guardian_name():
    return fake.first_name(), fake.last_name()

# Open the CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(1, num_records + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        gender = random_gender()
        birthdate = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age).strftime('%d.%m.%Y')
        email = fake.email()
        phone = fake.phone_number()
        address = fake.street_address()
        postal_code = fake.postcode()
        city = fake.city()
        guardian_first_name, guardian_last_name = random_guardian_name()
        guardian_phone = fake.phone_number()
        time_stamp = fake.date_time_between(start_date='-30y', end_date='now')

        writer.writerow({
            'id': i,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'birthdate': birthdate,
            'email': email,
            'phone': phone,
            'address': address,
            'postal_code': postal_code,
            'city': city,
            'guardian_first_name': guardian_first_name,
            'guardian_last_name': guardian_last_name,
            'guardian_phone': guardian_phone,
            'timestamp' : time_stamp
        })

print(f"{num_records} records have been generated and saved to {csv_file}.")
