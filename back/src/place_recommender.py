import requests
from flask import Flask, request, jsonify
from geopy.distance import geodesic
from openai import OpenAI

app = Flask(__name__)

# Sample data for demonstration
ml_data = {
    "category_1": [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060)],
    "category_2": [(41.8781, -87.6298), (51.5074, -0.1278), (45.4215, -75.6992)],
    "category_3": [(34.0522, -118.2437), (40.7128, -74.0060), (37.7749, -122.4194)],
    "category_4": [(51.5074, -0.1278), (45.4215, -75.6992), (41.8781, -87.6298)],
    "category_5": [(40.7128, -74.0060), (37.7749, -122.4194), (34.0522, -118.2437)],
    "category_6": [(45.4215, -75.6992), (41.8781, -87.6298), (51.5074, -0.1278)],
    "category_7": [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060)],
    "category_8": [(51.5074, -0.1278), (45.4215, -75.6992), (41.8781, -87.6298)],
    "category_9": [(34.0522, -118.2437), (40.7128, -74.0060), (37.7749, -122.4194)],
    "category_10": [(45.4215, -75.6992), (41.8781, -87.6298), (51.5074, -0.1278)],
}

# Yandex Maps API key
yandex_maps_api_key = "00986bf4-3f13-4e13-b5d5-3d7ae47a018e"

# ChatGPT API endpoint
chatgpt_api_key = "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"
client = OpenAI(api_key=chatgpt_api_key)

if not yandex_maps_api_key:
    raise ValueError("key 'yandex_maps_api_key' is not provided")
if not chatgpt_api_key:
    raise ValueError("key 'chatgpt_api_key' is not provided")


class GeoPoint:
    name = None
    description = None

    def __init__(self, coordinates=None):
        self.coordinates = coordinates
        self.set_name()
        self.set_description()

    def set_name(self, name=None):
        if name is None:
            self.name = get_location_name(self.coordinates)
        else:
            self.name = name

    def set_description(self, description=None):
        if description is None:
            self.description = get_description_from_chatgpt(self.name) if self.name is not None else "smthng untitled"
        else:
            self.description = description

    def get_point(self):
        return {
            "name": self.name,
            "coordinates": self.coordinates,
            "description": self.description,
        }


def get_location_name(coordinates):
    """
    Get the name of a location using Yandex Maps API.
    """
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={yandex_maps_api_key}&format=json&geocode={coordinates[1]},{coordinates[0]}"
    response = requests.get(url)
    data = response.json()
    print("Yandex answer")
    print(response.text)
    try:
        name = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
        return name
    except (KeyError, IndexError):
        return "Unknown Location"


def get_description_from_chatgpt(location_name):
    """
    Get a short description for a location using ChatGPT.
    """
    message = f" Чат, привет! Ты не мог бы рассказать мне про это место? Двух-трех преложений будет достаточно {location_name}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message.content


@app.route('/get_closest_coordinates', methods=['POST'])
def get_closest_coordinates():
    data = request.get_json()

    # Extract parameters from frontend
    user_category = data.get('category')
    user_coordinates = (data.get('latitude'), data.get('longitude'))

    # Get coordinates from ML based on the user's category
    ml_coordinates = ml_data.get(user_category, [])

    # Calculate distances and find the closest 3 coordinates
    distances = [(coord, geodesic(user_coordinates, coord).kilometers) for coord in ml_coordinates]
    closest_coordinates = sorted(distances, key=lambda x: x[1])[:3]

    # Extract only the coordinates from the result
    geo_points = [GeoPoint(coord[0]) for coord in closest_coordinates]

    return jsonify([point.get_point() for point in geo_points])


if __name__ == '__main__':
    app.run(debug=True)
