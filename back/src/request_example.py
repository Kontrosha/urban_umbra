import json

import requests

url = "http://kontrosha.pythonanywhere.com/get_closest_coordinates"
data = {
    "hotel": "Miramonti Boutique Hotel",
}

response = requests.post(url, json=data)

print(response.json())
with open('example.json', encoding='koi8-r', mode='w') as file:
    json.dump(response.json(), file)
