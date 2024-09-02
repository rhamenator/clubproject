from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import os # To check if the file(s) exist
import csv

club = "The club"


def submit_form():
    # Get user input from the form
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone = phone_entry.get()
    birth_date = birth_date_entry.get()
    address = address_entry.get()
    postal_code = postal_code_entry.get()
    guardian = guardian_entry.get()
    guardian_phone = guardian_phone_entry.get()

    # Get date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if club members club.csv file exists
    file_exists = os.path.isfile(f"club_members {club}.csv")

    with open(f"Club_members {club}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([first_name, last_name, phone, birth_date, address, postal_code, guardian, guardian_phone, timestamp])

    # Clear the form contents
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    birth_date_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    postal_code_entry.delete(0, tk.END)
    guardian_entry.delete(0, tk.END)
    guardian_phone_entry.delete(0, tk.END)

    # Show registration confirmation
    messagebox.showinfo("Registered", f"You are registered as a member of {club}!")

'''
    # For testing, show input data in the form as entered.
    first_name_entry.insert(0, f"First name: {first_name}")
    last_name_entry.insert(0, f"Last name: {last_name}")
    phone_entry.insert(0, f"Phone: {phone}")
    birth_date_entry.insert(0, f"Birth date: {birth_date}")
    address_entry.insert(0, f"Street name: {address}")
    postal_code_entry.insert(0, f"Postal code: {postal_code}")
    guardian_entry.insert(0, f"Guardian's name: {guardian}")
    guardian_phone_entry.insert(0, f"Guardian's phone: {guardian_phone}")
'''

def reset_form():
    # Reset all fields
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    birth_date_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    postal_code_entry.delete(0, tk.END)
    guardian_entry.delete(0, tk.END)
    guardian_phone_entry.delete(0, tk.END)

def toggle_fullscreen(event=None):
    '''Fullscreen Yes/No'''
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)


def exit_fullscreen(event):
    '''Exit fullscreen'''
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", is_fullscreen)

# Create main window + title and size of the window

root = tk.Tk()
root.title(f"Registration @ {club}")
'''root.geometry("800x600")''' # Set resolution if desired
root.attributes("-fullscreen", True) # Set program to fullscreen mode.

# Don't start in fullscreen because it's annoying
is_fullscreen = False
root.attributes("-fullscreen", is_fullscreen)
root.bind("<Escape>", exit_fullscreen) # Exit fullscreen
root.bind("<F11>", toggle_fullscreen) # Toggle fullscreen (on/off)

# Header in main window
header_label = tk.Label(root, text=f"{club}", font=("Arial", 16))
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# Change font and size
label_font = ("Arial", 14)
large_font = ("Arial", 14)
button_font = ("Arial", 14)

# Create and place labels and input fields
tk.Label(root, font=label_font, text="Fornavn: ").grid(row=1, column=0, padx=10, pady=10, sticky="e")
first_name_entry = tk.Entry(root, font=large_font)
first_name_entry.grid(row=1, column=1)

tk.Label(root, font=label_font, text="Etternavn: ").grid(row=2, column=0, padx=10, pady=10, sticky="e")
last_name_entry = tk.Entry(root, font=large_font)
last_name_entry.grid(row=2, column=1)

tk.Label(root, font=label_font, text="Telefon: ").grid(row=3, column=0, padx=10, pady=10, sticky="e")
phone_entry = tk.Entry(root, font=large_font)
phone_entry.grid(row=3, column=1)

tk.Label(root, font=label_font, text="Født: ").grid(row=4, column=0, padx=10, pady=10, sticky="e")
birth_date_entry = tk.Entry(root, font=large_font)
birth_date_entry.grid(row=4, column=1)

tk.Label(root, font=label_font, text="Gatenavn: ").grid(row=5, column=0, padx=10, pady=10, sticky="e")
address_entry = tk.Entry(root, font=large_font)
address_entry.grid(row=5, column=1)

tk.Label(root, font=label_font, text="Postnummer: ").grid(row=6, column=0, padx=10, pady=10, sticky="e")
postal_code_entry = tk.Entry(root, font=large_font)
postal_code_entry.grid(row=6, column=1)

tk.Label(root, font=label_font, text="Foresattes navn: ").grid(row=7, column=0, padx=10, pady=10, sticky="e")
guardian_entry = tk.Entry(root, font=large_font)
guardian_entry.grid(row=7, column=1)

tk.Label(root, font=label_font, text="Telefon til foresatt: ").grid(row=8, column=0, padx=10, pady=10, sticky="e")
guardian_phone_entry = tk.Entry(root, font=large_font)
guardian_phone_entry.grid(row=8, column=1)

# Buttons to either complete registration or clear the form
submit_button = tk.Button(root, font=button_font, text="Ferdig", command=submit_form)
submit_button.grid(row=10, column=0, pady=10, columnspan=2, sticky="e", padx=(0, 100))

reset_button = tk.Button(root, font=button_font, text="Slett", command=reset_form)
reset_button.grid(row=10, column=2, pady=10, columnspan=2, sticky="w", padx=(100, 0))

# Run the program
root.mainloop()
