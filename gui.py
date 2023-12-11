import os
import tkinter as tk
from tkinter import ttk, filedialog
import serial
from serial.tools import list_ports

# zmienna globalna do przechowywania obiektu serial
ser = None
port_info_displayed = False  # flaga informujaca, czy informacja o polaczeniu zostala wyswietlona
file_path_save = None  # sciezka do zapisywanego pliku
file_path_load = None  # sciezka do wczytanego pliku

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
        # nowe połączenie
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

def save_text_with_dialog():
    global file_path_save
    # jesli jeszcze nie wybrano pliku,ma sie otworzyc eksplorator
    if file_path_save is None:
        file_path_save = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    # zapisywanie tekstu do wybranego pliku
    if file_path_save:
        with open(file_path_save, 'a') as file:
            file.write(text_entry.get() + '\n')
        save_filename_label.config(text=f"Save Filename: {os.path.basename(file_path_save)}")

def load_text():
    global file_path_load
    # otwieranie eksploratora plikow
    file_path_load = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    # wczytanie tekstow z pliku
    if file_path_load:
        try:
            with open(file_path_load, 'r') as file:
                for line in file:
                    saved_texts_listbox.insert(tk.END, line.strip())
            load_filename_label.config(text=f"Load Filename: {os.path.basename(file_path_load)}")
        except FileNotFoundError:
            saved_texts_listbox.insert(tk.END, "No saved texts found.")

def clear_saved_texts():
    saved_texts_listbox.delete(0, tk.END)

# obsluga zdarzenia klikniecia na element z listy
def on_listbox_click(event):
    selected_text = saved_texts_listbox.get(saved_texts_listbox.curselection())
    text_entry.delete(0, tk.END)  # Wyczyść istniejący tekst w text_entry
    text_entry.insert(tk.END, selected_text)  # Wstaw zaznaczony tekst z listy do text_entry
    send_text_label.config(text="Text to send: ")

# odswiezanie portow po wpisaniu baudrate
def refresh_ports(event=None):
    global ser
    # zamknięcie poprzedniego połączenia, jeśli istniało
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
port_combobox.bind("<<ComboboxSelected>>", refresh_ports)  # dodanie zdarzenia zmiany wartosci

# zmienna do przechowywania wybranego portu
selected_port_var = tk.StringVar()
selected_port_entry = tk.Entry(root, textvariable=selected_port_var, state='readonly', width=10)
selected_port_entry.grid(row=0, column=2)

refresh_button = tk.Button(root, text="Refresh Ports", command=lambda: refresh_ports(None))  # dodawanie wywolania funkcji refresh_ports
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
baudrate_var.set("9600")  # domyślna prędkość transmisji
baudrate_entry.bind("<FocusOut>", lambda event: refresh_ports())  # wywolanie funkcji refresh_ports po stracie focusu z pola baudrate

# wysylanie tekstu do wyswietlacza
send_button = tk.Button(root, text="Send", command=send_to_display)
send_button.grid(row=2, column=2, pady=10)

# opcje wyboru trybu wyświetlacza
mode_label = tk.Label(root, text="Mode:")
mode_label.grid(row=3, column=0)
mode_combobox = ttk.Combobox(root, values=["Static", "Scrolling"])
mode_combobox.grid(row=3, column=1)
# domyslny tryb
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

# lista zapisanych tekstow
saved_texts_label = tk.Label(root, text="Saved Texts:")
saved_texts_label.grid(row=6, column=0)
saved_texts_listbox = tk.Listbox(root)
saved_texts_listbox.grid(row=6, column=1, columnspan=3, pady=10)

# zdarzenie klikniecia na element listy
saved_texts_listbox.bind("<ButtonRelease-1>", on_listbox_click)

# przycisk zapisywania tekstu
save_button = tk.Button(root, text="Save Text", command=save_text_with_dialog)
save_button.grid(row=7, column=0)

# Przycisk wczytywania zapisanych tekstow
load_button = tk.Button(root, text="Load Texts", command=load_text)
load_button.grid(row=7, column=1)

# button do czyszczenia listy
clear_button = tk.Button(root, text="Clear Texts", command=clear_saved_texts)
clear_button.grid(row=7, column=2)

# etykiety dla nazw plikow
save_filename_label = tk.Label(root, text="Save Filename: None")
save_filename_label.grid(row=8, column=0)

load_filename_label = tk.Label(root, text="Load Filename: None")
load_filename_label.grid(row=8, column=1)

# obsługa zdarzenia zmiany tekstu w baudrate
baudrate_var.trace_add("write", on_baudrate_entry_change)

root.mainloop()
