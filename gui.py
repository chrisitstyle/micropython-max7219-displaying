import tkinter as tk
from tkinter import ttk
import json
import serial
from serial.tools import list_ports

# Zmienna globalna do przechowywania obiektu Serial
ser = None
port_info_displayed = False  # flaga informująca, czy informacja o połączeniu została już wyświetlona

# Funkcje aplikacji
def send_to_display():
    global ser, port_info_displayed
    mode = mode_combobox.get()
    speed = speed_scale.get()
    brightness = brightness_scale.get()
    message = text_entry.get()

    # sprawdzenie czy wszystkie pola sa wypelnione
    if not selected_port_var.get() or not baudrate_var.get() or not message:
        print("Fill in all fields before sending.")
        return

    try:
        # nowe polaczenie
        baudrate = int(baudrate_var.get())
        ser = serial.Serial(selected_port_var.get(), baudrate)
        print(f"Connected to {selected_port_var.get()} with baudrate {baudrate}")
        port_info_displayed = True
    except serial.SerialException as e:
        print(f"Error connecting to {selected_port_var.get()} with baudrate {baudrate}: {e}")

    # Format: "mode;speed;brightness;message"
    data_to_send = f"{mode};{speed};{brightness};{message}\n"

    try:
        ser.write(data_to_send.encode('utf-8'))
        print("Sent to display:", data_to_send)
    except serial.SerialException as e:
        print("Error sending to display:", e)

def save_text():
    # zapisywanie tekstu do pliku
    with open('saved_texts.txt', 'a') as file:
        file.write(text_entry.get() + '\n')

def load_text():
    # wczytywane teksty z pliku
    try:
        with open('saved_texts.txt', 'r') as file:
            for line in file:
                saved_texts_listbox.insert(tk.END, line.strip())
    except FileNotFoundError:
        saved_texts_listbox.insert(tk.END, "No saved texts found.")

def refresh_ports(event=None):
    global ser
    # zamkniecie poprzedniego polaczenia, jesli istnialo
    if ser and ser.is_open:
        ser.close()

    # wybieranie portu z listy
    selected_port = port_combobox.get()
    selected_port_var.set(selected_port)

# odswiezanie portow po wpisaniu baudrate
def on_baudrate_entry_change(*args):
    # odswiezanie tylko po stracie focusu na polu baudrate
    refresh_ports()

# Konfiguracja GUI
root = tk.Tk()
root.title("MAX7219 - Display Controller by KP")
root.resizable(False, False)  # Blokowanie zmiany rozmiaru okna

# wybieranie portu COM
port_label = tk.Label(root, text="COM Port:")
port_label.grid(row=0, column=0)
available_ports = [port.device for port in list_ports.comports()]
port_combobox = ttk.Combobox(root, values=available_ports)
port_combobox.grid(row=0, column=1)
port_combobox.bind("<<ComboboxSelected>>", refresh_ports)  # dodanie zdarzenia zmiany wartości

# zmienna do przechowywania wybranego portu
selected_port_var = tk.StringVar()
selected_port_entry = tk.Entry(root, textvariable=selected_port_var, state='readonly', width=10)
selected_port_entry.grid(row=0, column=2)

refresh_button = tk.Button(root, text="Refresh Ports", command=lambda: refresh_ports(None))  # dodawanie wywołania funkcji refresh_ports
refresh_button.grid(row=0, column=3)


send_text_label = tk.Label(root, text="Text to send:")
send_text_label.grid(row=1, column=0)

# wprowadzanie tekstu do wyslania
text_entry = tk.Entry(root, width=35)
text_entry.grid(row=1, column=1, columnspan=3, pady=10)

# pole do wpisywania transmisji
baudrate_label = tk.Label(root, text="Baudrate:")
baudrate_label.grid(row=2, column=0)
baudrate_var = tk.StringVar()
baudrate_entry = tk.Entry(root, textvariable=baudrate_var, width=10)
baudrate_entry.grid(row=2, column=1)
baudrate_var.set("9600")  # domyslna predkosc transmisji
baudrate_entry.bind("<FocusOut>", lambda event: refresh_ports())  # wywolywanie funkcji refresh_ports po stracie focusu z pola baudrate

# wysylanie tekstu do wyswietlacza
send_button = tk.Button(root, text="Send", command=send_to_display)
send_button.grid(row=2, column=2, pady=10)

# opcje wyboru trybu wyswietlacza
mode_label = tk.Label(root, text="Mode:")
mode_label.grid(row=3, column=0)
mode_combobox = ttk.Combobox(root, values=["Static", "Scrolling"])
mode_combobox.grid(row=3, column=1)
# ustawienie domyslnego trybu
mode_combobox.set("Scrolling")

# suwak do szybkosci tekstu
speed_label = tk.Label(root, text="Speed:")
speed_label.grid(row=4, column=0)
speed_scale = tk.Scale(root, from_=0, to=100, orient='horizontal')
speed_scale.grid(row=4, column=1, columnspan=3, pady=10)

# suwak do jasnosci wyswietlacza
brightness_label = tk.Label(root, text="Brightness:")
brightness_label.grid(row=5, column=0)
brightness_scale = tk.Scale(root, from_=0, to=15, orient='horizontal')
brightness_scale.grid(row=5, column=1, columnspan=3, pady=10)

# lista zapisanych tekstów
saved_texts_label = tk.Label(root, text="Saved Texts:")
saved_texts_label.grid(row=6, column=0)
saved_texts_listbox = tk.Listbox(root)
saved_texts_listbox.grid(row=6, column=1, columnspan=3, pady=10)

# przycisk zapisywania tekstu
save_button = tk.Button(root, text="Save Text", command=save_text)
save_button.grid(row=7, column=0)

# Przycisk wczytywania zapisanych tekstów
load_button = tk.Button(root, text="Load Texts", command=load_text)
load_button.grid(row=7, column=1)

# obsluga zdarzenia zmiany tekstu w polu "Baudrate"
baudrate_var.trace_add("write", on_baudrate_entry_change)

root.mainloop()
