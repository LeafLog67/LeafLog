# 🌿 LeafLog: Botanický Systém Triedy

LeafLog je interaktívny webový dashboard pre monitorovanie izbových rastlín v školských triedach. Systém spája reálne dáta z hardvéru (Arduino/ESP32) s užitočnými funkciami pre žiakov a týždenníkov.

## ✨ Hlavné funkcie
* **Live Dashboard:** Sledovanie teploty vzduchu, vlhkosti vzduchu a vlhkosti pôdy v reálnom čase.
* **Historické grafy:** Prehľadné zobrazenie vývoja mikroklímy pomocou knižnice Chart.js.
* **Systém pre týždenníkov:** Digitálna tabuľa služieb na 4 týždne dopredu, ktorú je možné upravovať priamo cez prehliadač.
* **Kontrolka polievania:** Tlačidlo „Označiť ako poliate“, ktoré neskresľuje dáta v grafe, ale slúži ako vizuálna značka pre ostatných spolužiakov, že kvet už bol dnes poliaty.
* **Trvalé ukladanie dát:** Všetky názvy rastlín, mená týždenníkov, história meraní a stavy tlačidiel sa ukladajú do súboru `databaza.json` a nezmažú sa ani po reštarte servera.

## 🛠️ Použité technológie
* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3 (Moderný sklenený dizajn / Glassmorphism), JavaScript (Vanilla)
* **Grafy:** Chart.js v3
* **Ukladanie dát:** JSON Databáza

## 🚀 Ako projekt spustiť lokálne

1. **Stiahni alebo naklonuj tento repozitár:**
   ```bash
   git clone <link-na-tvoj-github-repozitar>
   cd leaflog
