import json
import os
import pickle
import sys
import time
from datetime import datetime

from openai import OpenAI

# Determine the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "../../../")
sys.path.append(project_root)

# Read keys from the configuration file
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '../keys/config.json')

with open(file_path) as config_file:
    config = json.load(config_file)

# Retrieve the OpenAI API key from the configuration
chatgpt_api_key = config['OPEN_AI_KEY']
client = OpenAI(api_key=chatgpt_api_key)


def get_description_from_chatgpt(place_name, place_location):
    """
    Get a short description for a location using ChatGPT.
    """
    start_time = datetime.now()
    print("Asking ChatGPT")

    # Define a message to request information about a location from ChatGPT
    message = f" Чат, привет! Ты не мог бы рассказать мне про это место в Австрии, Тироле, {place_name}, в {place_location}? Двух-трех предложений будет достаточно."
    try:
        # Send a message to ChatGPT and retrieve the response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message},
            ],
        )
        end_time = datetime.now()
        print("Chat has answered in", end_time - start_time)
        return response.choices[0].message.content
    except:
        print("Error RateLimitError: Превышен лимит запросов. Попробуйте позже.")
        return ""


# Determine the path to the recommender pickle file
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '../../../recommender/front/recommender.pkl')

# Load the recommender data from the pickle file
with open(file_path, 'rb') as f:
    rec = pickle.load(f)

# Get the total number of recommendations
line_count = len(rec['object_metadata']['name'])
print(line_count)

# Initialize a list to track errors during the description retrieval process
errors = [x for x in range(line_count)]

# Continuously retrieve descriptions until there are no errors left
while len(errors) != 0:
    repeats = errors
    l_repeats = len(repeats)
    pos = 0
    errors = []
    all = {}
    print("Starting again with size: ", l_repeats)
    for ind in repeats:
        if ind % 100 == 0 and ind != 0:
            print("Waiting because we already sent 50 requests")
            time.sleep(20)  # wait in seconds
        print("Done", ind, "where is", pos, "of", l_repeats)

        recommendation = {}
        name = rec['object_metadata']['name'][ind]
        location = rec['object_metadata']['location'][ind]

        # Retrieve a description using ChatGPT
        recommendation['description'] = get_description_from_chatgpt(name, location)

        if recommendation['description'] == "":
            errors.append(ind)
        else:
            all[name] = recommendation
        print(name, location)
        pos += 1

    # Append the retrieved descriptions to a JSON file
    with open("description.json", 'a') as file:
        json.dump(all, file)

    print("Failed indexes are", errors)
