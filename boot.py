import machine
import time
from circular_buffer import CircularBuffer
import max7219

# inicjalizacja UARTa
uart = machine.UART(2, baudrate=115200, tx=17, rx=16)

# Konfiguracja interfejsu SPI
spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0)

# Inicjalizacja wyświetlacza MAX7219
display = max7219.Max7219(32, 8, spi, machine.Pin(15))

# Funkcje sterujące wyświetlaczem
def scroll_text(text, speed):
    for i in range(32, -(len(text) * 8), -1):
        display.fill(0)
        display.text(text, i, 0, 1)
        display.show()
        time.sleep_ms(speed)

def display_static_text(text):
    display.fill(0)
    display.text(text, 0, 0, 1)
    display.show()

# Zmienna do przechowywania aktualnego tekstu
current_message = ""
# Inicjalizacja zmiennej 'mode'
mode = ""

# Główna pętla
while True:
    if uart.any():
        received_data = uart.readline().decode('utf-8').strip()
        mode, speed, brightness, message = received_data.split(';')

        # Ustawienia jasności
        if int(brightness) == 0:
            # ustawiebie minimalnej jasnosci
            display.brightness(1)
        else:
            display.brightness(int(brightness))

        # aktualizowanie tekstu
        current_message = message

    # wyswietlanie tekstu
    if mode == 'Scrolling':
        # przypadek, jesli speed = 0
        if int(speed) == 0:
            
            mode = 'Static'
        else:
            
            scroll_text(current_message, 100 - int(speed))
    elif mode == 'Static':
        display_static_text(current_message)
