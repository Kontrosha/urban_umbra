import json

import requests

url = "http://127.0.0.1:5000/get_closest_coordinates"
data = {
    "category": "category_1",
    "latitude": 37.7749,
    "longitude": -122.4194
}

response = requests.post(url, json=data)

print(response.json())
with open('example.json', encoding='koi8-r', mode='w') as file:
    json.dump(response.json(), file)