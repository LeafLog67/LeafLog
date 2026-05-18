import serial
import time
import requests

# NASTAVENIE: Skontroluj, či ti sedí COM port podľa Arduino IDE
ARDUINO_PORT = 'COM11' 
BAUD_RATE = 9600
FLASK_URL = 'http://127.0.0.1:5000/api/data'

print("Pripájam sa na Arduino...")
try:
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Krátka pauza na reštart Arduina po pripojení
    print("Pripojené úspešne! Čítam dáta...")
except Exception as e:
    print(f"Chyba pripojenia: {e}")
    exit()

while True:
    try:
        # KLUČOVÝ KROK: Pred čítaním zahodíme všetky staré správy, čo sa nazbierali v pamäti, kým skript spal
        ser.reset_input_buffer()
        time.sleep(0.5)  # Krátka pauzička, aby stihol doraziť úplne nový, čerstvý riadok
        
        if ser.in_waiting > 0:
            # Čítanie najnovšieho riadku z Arduina
            line = ser.readline().decode('utf-8').strip()
            
            # Kontrola, či riadok obsahuje očakávané kľúčové slová
            if "TEPLOTA:" in line and "|PODA:" in line:
                print(f"Čerstvé dáta z Arduina: {line}")
                
                # Rozsekneme text podľa znaku '|'
                casti = line.split('|')
                
                # Vytiahneme konkrétne hodnoty
                teplota = casti[0].split(':')[1]
                vzduch = casti[1].split(':')[1]
                
                # Bezpečné vytiahnutie pôdy
                poda_surova = casti[2].split('PODA:')[1]
                poda = poda_surova.split('%')[0].strip()
                
                # Príprava dát pre Flask
                payload = {
                    "teplota": teplota,
                    "vzduch": vzduch,
                    "poda": poda
                }
                
                # Odoslanie dát cez POST na Flask server
                response = requests.post(FLASK_URL, json=payload)
                print(f"Odoslané do Flasku, status: {response.status_code}")
                
                # Po úspešnom odoslaní počkáme 1 minútu
                time.sleep(60)
                
    except Exception as e:
        print(f"Chyba počas behu: {e}")
        time.sleep(1)