import requests
import pandas as pd
from io import StringIO

# URL pliku CSV
url = "https://api.dane.gov.pl/1.4/resources/56169,zdarzenia-w-ruchu-drogowych-w-2023-r-sprawcy-pojazd-uczestnika?lang=pl"

# Pobranie danych
response = requests.get(url)

# Sprawdzenie, czy pobrano poprawnie
if response.status_code == 200:
    csv_data = StringIO(response.text)  # Konwersja do formatu pliku tekstowego
    df = pd.read_csv(csv_data, sep=";")  # Wczytanie CSV do pandas
    print(df.head())  # Podgląd pierwszych wierszy
else:
    print(f"Błąd pobierania: {response.status_code}")

