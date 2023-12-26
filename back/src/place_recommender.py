import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "../../")
sys.path.append(project_root)

import requests
import json
from flask import Flask, request, jsonify
from openai import OpenAI
from urban_umbra.recommender.front.recommend import Recommender

app = Flask(__name__)

# Read keys from config
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'openapi')

with open('keys/config.json') as config_file:
    config = json.load(config_file)

chatgpt_api_key = config['OPEN_AI_KEY']
client = OpenAI(api_key=chatgpt_api_key)

# Yandex Maps API key
yandex_maps_api_key = config['YANDEX_MAPS_KEY']

if not yandex_maps_api_key:
    raise ValueError("key 'yandex_maps_api_key' is not provided")
if not chatgpt_api_key:
    raise ValueError("key 'chatgpt_api_key' is not provided")


class GeoPoint:
    name = None
    description = "empty"
    coordinates = None

    def __init__(self, name=None, location=None, reviews=None):
        self.name = name
        self.location = location
        self.set_coordinates()
        self.set_description()
        self.reviews = self.total_review(reviews)

    def set_coordinates(self, coordinates=None):
        if coordinates is None:
            self.coordinates = get_location_coordinates(self.location + " " + self.name)
        else:
            self.coordinates = coordinates

    def set_description(self, description=None):
        if description is None:
            self.description = get_description_from_chatgpt(self.name) if self.name is not None else "smthng untitled"
        else:
            self.description = description

    # TODO @Kontrosha: rethink sending requests
    def total_review(self, reviews):
        # if reviews:
        #     all_reviews = ' '.join(reviews)
        #     return get_summury_review_from_chatgpt(self.name, all_reviews)
        # else:
        return "No reviews"

    def get_point(self):
        return {
            "name": self.name,
            "coordinates": self.coordinates,
            "description": self.description,
            "review": self.reviews
        }


def get_location_coordinates(name):
    """
    Get the name of a location using Yandex Maps API.
    """
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={yandex_maps_api_key}&format=json&geocode=Австрия+Тироль+{name.lower()}"
    response = requests.get(url)
    data = response.json()
    try:
        coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(
            ' ')
        return coordinates[1], coordinates[0]
    except (KeyError, IndexError):
        return "Unknown Location"


def get_description_from_chatgpt(location_name):
    """
    Get a short description for a location using ChatGPT.
    """
    message = f" Чат, привет! Ты не мог бы рассказать мне про это место в Австрии, Тироле, {location_name}? Двух-трех преложений будет достаточно."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message.content


def get_summury_review_from_chatgpt(location_name, all_reviews):
    """
    Get a short description for a location using ChatGPT.
    """
    message = f" Чат, привет! Ты не мог сделать краткий отзыв-выжимику этих отзывов {all_reviews} о месте {location_name} в Австрии, Тироль. Только выбери хорошие, пожалуйста, также ограничься 1-2 предложениями."
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
    user_hotel = data.get('hotel')

    # Get coordinates from ML based on the user's category
    recommendator = Recommender()
    recommended_places = recommendator.recommend(user_hotel)

    with open('example_answer.json', encoding='koi8-r', mode='w') as file:
        json.dump(recommended_places, file)

    geo_points = [GeoPoint(place['name'], place['location'], place['reviews']) for place in recommended_places]

    return jsonify([point.get_point() for point in geo_points])


if __name__ == '__main__':
    app.run(debug=True)
