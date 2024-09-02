from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import os #For å sjekke om filen(e) eksisterer
import csv

klubb = "The club"


def submit_form():
    #Hent brukerens input fra formen
    navn = navn_entry.get()
    enavn = enavn_entry.get()
    tlf = tlf_entry.get()
    fodt = fodt_entry.get()
    adresse = adresse_entry.get()
    postnr = postnr_entry.get()
    foresatt = foresatt_entry.get()
    foresattnr = foresattnr_entry.get()



    #Hente dato og klokkeslett
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #Se om klubbmedlemmer klubb.csv filen eksisterer
    file_exists = os.path.isfile(f"klubbmedlemmer {klubb}.csv")

    with open(f"Klubbmedlemmer {klubb}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([navn, enavn, tlf, fodt, adresse, postnr, foresatt, foresattnr, timestamp])


    #Slett innholdet i forment
    navn_entry.delete(0, tk.END)
    enavn_entry.delete(0, tk.END)
    tlf_entry.delete(0, tk.END)
    fodt_entry.delete(0, tk.END)
    adresse_entry.delete(0, tk.END)
    postnr_entry.delete(0, tk.END)
    foresatt_entry.delete(0, tk.END)
    foresattnr_entry.delete(0, tk.END)



    #Vis bekreftelse på registrering
    messagebox.showinfo("Registrert", f"Du er registrert som medlem på {klubb}!")

'''
    #For testing, vis input data i formene dem er blitt skrevet i.
    navn_entry.insert(0, f"Navn: {navn}")
    enavn_entry.insert(0, f"Etternavn: {enavn}")
    tlf_entry.insert(0, f"Telefon: {tlf}")
    fodt_entry.insert(0, f"Født: {fodt}")
    adresse_entry.insert(0, f"Gatenavn: {adresse}")
    postnr_entry.insert(0, f"Postnummer: {postnr}")
    foresatt_entry.insert(0, f"Foresattes navn: {foresatt}")
    foresattnr_entry.insert(0, f"Telefon til foresatt: {foresattnr}")
'''

def reset_form():
    # Nullstill alle felt
    navn_entry.delete(0, tk.END)
    enavn_entry.delete(0, tk.END)
    tlf_entry.delete(0, tk.END)
    fodt_entry.delete(0, tk.END)
    adresse_entry.delete(0, tk.END)
    postnr_entry.delete(0, tk.END)
    foresatt_entry.delete(0, tk.END)
    foresattnr_entry.delete(0, tk.END)

def toggle_fullscreen(event=None):
    '''Fullscreen Ja/Nei'''
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)


def exit_fullscreen(event):
    '''Går ut av fullscreen'''
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", is_fullscreen)

# Opprett hovedvinduet + tittel og størrelse på vinduet

root = tk.Tk()
root.title(f"Registrering @ {klubb}")
'''root.geometry("800x600")''' #Angi oppløsning om du ønsker det
root.attributes("-fullscreen", True) #Setter programmet i fullskjermmodus.


#Start i fullscreen
is_fullscreen = True
root.attributes("-fullscreen", is_fullscreen)
root.bind("<Escape>", exit_fullscreen) #Går ut av fullskjerm
root.bind("<F11>", toggle_fullscreen) #Bytter mellom fullskjerm (av/på)

#Overskrift i hovedvinduet
header_label = tk.Label(root, text=f"{klubb}", font=("Arial", 16))
header_label.grid(row=0, column=0, columnspan=2, pady=10)


#Endre font og størrelse
label_font = ("Arial", 14)
large_font = ("Arial", 14)
button_font = ("Arial", 14)

#Lag og plasser labels og input feltene
tk.Label(root, font=label_font, text="Fornavn: ").grid(row=1, column=0, padx=10, pady=10, sticky="e")
navn_entry = tk.Entry(root, font=large_font)
navn_entry.grid(row=1, column=1)

tk.Label(root, font=label_font, text="Etternavn: ").grid(row=2, column=0, padx=10, pady=10, sticky="e")
enavn_entry = tk.Entry(root, font=large_font)
enavn_entry.grid(row=2, column=1)

tk.Label(root, font=label_font, text="Telefon: ").grid(row=3, column=0, padx=10, pady=10, sticky="e")
tlf_entry = tk.Entry(root, font=large_font)
tlf_entry.grid(row=3, column=1)

tk.Label(root, font=label_font, text="Født: ").grid(row=4, column=0, padx=10, pady=10, sticky="e")
fodt_entry = tk.Entry(root, font=large_font)
fodt_entry.grid(row=4, column=1)

tk.Label(root, font=label_font, text="Gatenavn: ").grid(row=5, column=0, padx=10, pady=10, sticky="e")
adresse_entry = tk.Entry(root, font=large_font)
adresse_entry.grid(row=5, column=1)

tk.Label(root, font=label_font, text="Postnummer: ").grid(row=6, column=0, padx=10, pady=10, sticky="e")
postnr_entry = tk.Entry(root, font=large_font)
postnr_entry.grid(row=6, column=1)

tk.Label(root, font=label_font, text="Foresattes navn: ").grid(row=7, column=0, padx=10, pady=10, sticky="e")
foresatt_entry = tk.Entry(root, font=large_font)
foresatt_entry.grid(row=7, column=1)

tk.Label(root, font=label_font, text="Telefon til foresatt: ").grid(row=8, column=0, padx=10, pady=10, sticky="e")
foresattnr_entry = tk.Entry(root, font=large_font)
foresattnr_entry.grid(row=8, column=1)



#Knapper for enten å fullføre registreringen eller tømme formen
submit_button = tk.Button(root, font=button_font, text="Ferdig", command=submit_form)
submit_button.grid(row=10, column=0, pady=10, columnspan=2, sticky="e", padx=(0, 100))

reset_button = tk.Button(root, font=button_font, text="Slett", command=reset_form)
reset_button.grid(row=10, column=2, pady=10, columnspan=2, sticky="w", padx=(100, 0))



#Kjør programmet
root.mainloop()
