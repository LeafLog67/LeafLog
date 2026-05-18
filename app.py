from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

DB_FILE = "databaza.json"

# PREDVOLENÉ DÁTA (Použijú sa iba úplne prvýkrát)
predvolene_rastliny = {
    "rastlina1": {
        "id": "rastlina1", "nazov": "🌿 Klikni a zadaj názov 1",
        "aktualne": {"teplota": "0.0", "vzduch": "0", "poda": "0", "stav": "🚨 SUCHÁ (Zatiaľ bez dát)", "cas": "--:--"},
        "historia": [], "manualne_poliate": ""  
    },
    "rastlina2": {
        "id": "rastlina2", "nazov": "🌸 Klikni a zadaj názov 2",
        "aktualne": {"teplota": "0.0", "vzduch": "0", "poda": "0", "stav": "🚨 SUCHÁ (Zatiaľ bez dát)", "cas": "--:--"},
        "historia": [], "manualne_poliate": ""
    },
    "rastlina3": {
        "id": "rastlina3", "nazov": "🌵 Klikni a zadaj názov 3",
        "aktualne": {"teplota": "0.0", "vzduch": "0", "poda": "0", "stav": "🚨 SUCHÁ (Zatiaľ bez dát)", "cas": "--:--"},
        "historia": [], "manualne_poliate": ""
    }
}

predvoleny_kalendar = []
start_tyzdna = datetime.now()
for i in range(4):
    koniec_tyzdna = start_tyzdna + timedelta(days=7)
    predvoleny_kalendar.append({
        "index": i, "tyzden": f"{start_tyzdna.strftime('%d.%m.')} - {koniec_tyzdna.strftime('%d.%m.%Y')}", "sluzba": ""
    })
    start_tyzdna = koniec_tyzdna

def nacitaj_datu():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # Kontrola, či súbor obsahuje všetko potrebné, aby kód nespadol
                if "rastliny" in data and "kalendar" in data:
                    return data
            except:
                pass
    return {"rastliny": predvolene_rastliny, "kalendar": predvoleny_kalendar}

def uloz_datu(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

system_data = nacitaj_datu()

@app.route('/')
def index():
    global system_data
    system_data = nacitaj_datu()
    return render_template('index.html', rastliny=system_data["rastliny"], kalendar=system_data["kalendar"])

@app.route('/api/update_plant', methods=['POST'])
def update_plant():
    data = request.json
    rid = data.get("id")
    novy_nazov = data.get("nazov", "").strip()
    
    if rid in system_data["rastliny"] and novy_nazov:
        system_data["rastliny"][rid]["nazov"] = novy_nazov
        uloz_datu(system_data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/api/update_weeks', methods=['POST'])
def update_weeks():
    data = request.json
    idx = int(data.get("index", -1))
    nove_meno = data.get("sluzba", "").strip()
    
    if 0 <= idx < len(system_data["kalendar"]):
        system_data["kalendar"][idx]["sluzba"] = nove_meno
        uloz_datu(system_data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/api/data', methods=['POST'])
def prijmi_data():
    data = request.json
    if not data:
        return jsonify({"status": "error"}), 400
    
    rid = data.get("rastlina_id", "rastlina1")
    if rid in system_data["rastliny"]:
        teraz = datetime.now().strftime("%H:%M:%S")
        poda_hodnota = int(data['poda'])
        
        if poda_hodnota < 40:
            stav = "🚨 SUCHÁ (Treba zaliať!)"
        elif poda_hodnota > 85:
            stav = "💧 PRELIATA"
        else:
            stav = "MOKRÁ (V poriadku)"
            system_data["rastliny"][rid]["manualne_poliate"] = ""

        aktualny_balicek = {
            "teplota": data['teplota'], "vzduch": data['vzduch'], "poda": poda_hodnota, "stav": stav, "cas": teraz
        }
        system_data["rastliny"][rid]["aktualne"] = aktualny_balicek
        system_data["rastliny"][rid]["historia"].append(aktualny_balicek)
        
        if len(system_data["rastliny"][rid]["historia"]) > 30:
            system_data["rastliny"][rid]["historia"].pop(0)
            
        uloz_datu(system_data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

@app.route('/api/history/<rastlina_id>')
def daj_historiu(rastlina_id):
    # Znova načítame z disku, aby sme mali istotu, že posielame reálnu históriu po reštarte
    aktualne_data = nacitaj_datu()
    if rastlina_id in aktualne_data["rastliny"]:
        return jsonify({
            "aktualne": aktualne_data["rastliny"][rastlina_id]["aktualne"], 
            "historia": aktualne_data["rastliny"][rastlina_id]["historia"],
            "manualne_poliate": aktualne_data["rastliny"][rastlina_id]["manualne_poliate"]
        })
    return jsonify({"error": "Nenájdené"}), 404

@app.route('/api/zaliate/<rastlina_id>', methods=['POST'])
def zaliate(rastlina_id):
    if rastlina_id in system_data["rastliny"]:
        teraz = datetime.now().strftime("%H:%M")
        system_data["rastliny"][rastlina_id]["manualne_poliate"] = teraz  
        uloz_datu(system_data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
