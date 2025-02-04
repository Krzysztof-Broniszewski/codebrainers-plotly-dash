import requests

URL = "https://api.nbp.pl/api/cenyzlota/2024-01-01/2024-12-31/?format=json"

response = requests.get(URL)
data = response.json()

print(data)
