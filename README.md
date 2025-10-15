# 🚦 Interaktywny wykres: Wypadki drogowe w Polsce (Dash + Colab)

https://colab.research.google.com/github/Krzysztof-Broniszewski/codebrainers-plotly-dash/blob/main/plotly_dash_wypadki.ipynb

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](
  https://colab.research.google.com/github/Krzysztof-Broniszewski/codebrainers-plotly-dash/blob/main/plotly_dash_wypadki.ipynb
)

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
