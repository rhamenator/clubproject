import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import csv

# Define the SQLite database and table name
db_name = 'club_tracking.db'
table_name = 'members'

# Define the button padding constant
BUTTON_PADDING = 8

# Create the SQLite database and table if it doesn't exist
def create_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
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
    conn.commit()
    conn.close()

# Insert a record into the SQLite database
def insert_record(data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(f'''
        INSERT INTO {table_name} (
            first_name, last_name, gender, birthdate, email, phone, 
            address, postal_code, city, guardian_first_name, guardian_last_name, guardian_phone, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data + (timestamp,))
    conn.commit()
    conn.close()

# Append a record to the CSV file
def append_to_csv(data):
    with open('members.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'id', 'first_name', 'last_name', 'gender', 'birthdate', 'email', 'phone', 
            'address', 'postal_code', 'city', 'guardian_first_name', 'guardian_last_name', 'guardian_phone', 'timestamp'
        ])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow(dict(zip(writer.fieldnames, [None] + list(data) + [timestamp])))

# Function to handle member signup
def submit_form():
    birthdate = birthdate_entry.get()
    try:
        birthdate_obj = datetime.strptime(birthdate, '%d.%m.%Y')
        age = (datetime.now() - birthdate_obj).days // 365
    except ValueError:
        messagebox.showwarning("Feil", "Ugyldig fødselsdato. Bruk formatet DD.MM.YYYY.")
        return

    if age > 20:
        messagebox.showwarning("Feil", "Medlemmer må være 20 år eller yngre.")
        return

    data = (
        first_name_entry.get(),
        last_name_entry.get(),
        gender_var.get(),
        birthdate,
        email_entry.get(),
        phone_entry.get(),
        address_entry.get(),
        postal_code_entry.get(),
        city_entry.get(),
        guardian_first_name_entry.get() if age < 18 else None,
        guardian_last_name_entry.get() if age < 18 else None,
        guardian_phone_entry.get() if age < 18 else None
    )

    if all(data[:1]) and all(data[3:9]) and (age >= 18 or all(data[9:12])):
        insert_record(data)
        append_to_csv(data)
        messagebox.showinfo("Suksess", "Du har registrert deg!")
        clear_form()
    else:
        messagebox.showwarning("Feil", "Vennligst fyll ut alle nødvendige feltene.")

# Function to clear the form
def clear_form():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    gender_var.set('')
    birthdate_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    postal_code_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    guardian_first_name_entry.delete(0, tk.END)
    guardian_last_name_entry.delete(0, tk.END)
    guardian_phone_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Medlemsregistrering")

# Create and place the form fields
tk.Label(root, text="Fornavn:").grid(row=0, column=0, padx=10, pady=5)
first_name_entry = tk.Entry(root, width=20)
first_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Etternavn:").grid(row=1, column=0, padx=10, pady=5)
last_name_entry = tk.Entry(root, width=20)
last_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Kjønn:").grid(row=2, column=0, padx=10, pady=5)
gender_var = tk.StringVar()
gender_options = ["Mann", "Kvinne"]
gender_menu = tk.OptionMenu(root, gender_var, *gender_options)
gender_menu.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Fødselsdato (DD.MM.YYYY):").grid(row=3, column=0, padx=10, pady=5)
birthdate_entry = tk.Entry(root, width=20)
birthdate_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="E-post:").grid(row=4, column=0, padx=10, pady=5)
email_entry = tk.Entry(root, width=20)
email_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Telefon:").grid(row=5, column=0, padx=10, pady=5)
phone_entry = tk.Entry(root, width=20)
phone_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Adresse:").grid(row=6, column=0, padx=10, pady=5)
address_entry = tk.Entry(root, width=20)
address_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Postnummer:").grid(row=7, column=0, padx=10, pady=5)
postal_code_entry = tk.Entry(root, width=20)
postal_code_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="By:").grid(row=8, column=0, padx=10, pady=5)
city_entry = tk.Entry(root, width=20)
city_entry.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="Foresattes fornavn:").grid(row=9, column=0, padx=10, pady=5)
guardian_first_name_entry = tk.Entry(root, width=20)
guardian_first_name_entry.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Foresattes etternavn:").grid(row=10, column=0, padx=10, pady=5)
guardian_last_name_entry = tk.Entry(root, width=20)
guardian_last_name_entry.grid(row=10, column=1, padx=10, pady=5)

tk.Label(root, text="Foresattes telefon:").grid(row=11, column=0, padx=10, pady=5)
guardian_phone_entry = tk.Entry(root, width=20)
guardian_phone_entry.grid(row=11, column=1, padx=10, pady=5)

# Create and place the submit and clear buttons
submit_button = tk.Button(root, text="Registrer", command=submit_form)
submit_button.grid(row=12, column=0, pady=10, padx=(BUTTON_PADDING * 8, 0), sticky="w")

clear_button = tk.Button(root, text="Tøm", command=clear_form)
clear_button.grid(row=12, column=1, pady=10, padx=(0, BUTTON_PADDING * 8), sticky="e")

# Run the Tkinter event loop
root.mainloop()
