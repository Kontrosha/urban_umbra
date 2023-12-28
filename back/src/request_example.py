import json
from datetime import datetime

import requests

url = "http://kontrosha.pythonanywhere.com/get_closest_coordinates"
data = {
    "hotel": "Miramonti Boutique Hotel",
}
start_time = datetime.now()
response = requests.post(url, json=data)
end_time = datetime.now()
print(f"Receive answer in, {end_time}, it took {end_time - start_time}")
print(response.json())
with open('example.json', encoding='koi8-r', mode='w') as file:
    json.dump(response.json(), file)
