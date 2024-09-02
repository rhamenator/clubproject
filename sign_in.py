import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import csv

# Define the SQLite database and table names
db_name = 'club_tracking.db'
members_table = 'members'
sign_in_table = 'sign_in'

# Define the button padding constant
BUTTON_PADDING = 8

# Create the sign_in table if it doesn't already exist
def create_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {sign_in_table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Check if the phone number exists in the members table
def phone_exists(phone):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT 1 FROM {members_table} WHERE phone = ?
    ''', (phone,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Insert a record into the sign-in table
def insert_record(phone):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(f'''
        INSERT INTO {sign_in_table} (phone, timestamp)
        VALUES (?, ?)
    ''', (phone, timestamp))
    conn.commit()
    conn.close()

# Append a record to the CSV file
def append_to_csv(phone):
    with open('sign_in.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'phone', 'timestamp'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow({'id': None, 'phone': phone, 'timestamp': timestamp})

# Function to handle sign-in
def sign_in():
    phone = phone_entry.get()
    if phone:
        if phone_exists(phone):
            insert_record(phone)
            append_to_csv(phone)
            messagebox.showinfo("Suksess", "Du har sjekket inn!")
            phone_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Feil", "Telefonnummeret finnes ikke. Vennligst registrer deg først.")
    else:
        messagebox.showwarning("Feil", "Vennligst skriv inn telefonnummeret ditt.")

# Create the main window
root = tk.Tk()
root.title("Medlem Sjekk-Inn")

# Create and place the phone number label and entry
tk.Label(root, text="Telefonnummer:").grid(row=0, column=0, padx=10, pady=10)
phone_entry = tk.Entry(root, width=20)
phone_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the sign-in button
sign_in_button = tk.Button(root, text="Sjekk Inn", command=sign_in)
sign_in_button.grid(row=1, column=0, pady=10, padx=(BUTTON_PADDING * 8, 0), sticky="w")

# Create and place the clear button
clear_button = tk.Button(root, text="Tøm", command=lambda: phone_entry.delete(0, tk.END))
clear_button.grid(row=1, column=1, pady=10, padx=(0, BUTTON_PADDING * 8), sticky="e")

# Run the Tkinter event loop
root.mainloop()
