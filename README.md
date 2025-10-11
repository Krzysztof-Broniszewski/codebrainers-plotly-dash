# 🚦 Interaktywny wykres: Wypadki drogowe w Polsce (Dash + Colab)

[![Open in Colab](https://img.shields.io/badge/Open%20in-Colab-orange?logo=googlecolab)](https://colab.research.google.com/drive/1C2317YWBbP6fwRyGjI2sA-WHDHhmWEDG?usp=sharing)
[![Dash](https://img.shields.io/badge/Dash-latest-1f77b4)](#wymagania)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#wymagania)

Aplikacja **Dash** rysująca interaktywne wykresy liczby wypadków, ofiar śmiertelnych i rannych w Polsce na podstawie danych z **Google Sheets**. 
Kod jest przygotowany pod **Google Colab** – działa bez `JupyterDash`, korzystając z czystego **Dash** i proxy portu Colaba.

---

## ✨ Funkcje
- Pobieranie danych z Google Sheets (CSV/XLSX fallback).
- Automatyczne wykrywanie wiersza nagłówka i nazw kolumn (odporność na zmiany w arkuszu).
- Interaktywny **RangeSlider** (zakres lat) i **Checklist** (wybór serii).
- Estetyczny wykres liniowy (Plotly).
- Działa **inline** w Colabie dzięki uruchomieniu serwera w tle + proxy.

---

## 🧰 Wymagania
- Python **3.10+**
- Biblioteki: `dash`, `plotly`, `pandas`, `requests`, `unidecode`, `openpyxl`

W Colabie instalacja odbywa się automatycznie w kodzie:
```python
!pip -q install dash plotly unidecode openpyxl requests pandas

# ważne: nowszy Dash → używaj app.run, nie app.run_server
PORT = 8050
app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

# w Colabie wyświetlamy aplikację przez proxy:
from google.colab.output import eval_js
from IPython.display import IFrame, display
url = eval_js(f"google.colab.kernel.proxyPort({PORT})")
display(IFrame(src=url, width="100%", height=600))
