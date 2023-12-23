import pickle
from scipy.sparse.linalg import svds
import numpy as np
import heapq
import random

# number of recommendations
num_indices = 10 

with open('recommender.pkl', 'rb') as f:
    rec = pickle.load(f)

def scale_values(values):
    min_value = min(values)
    _values = [value - min_value for value in values]
    max_value = max(_values)
    _values = [value/max_value for value in _values]
    _valus = [1 - value for value in _values]
    return _values

def get_top_n_indices(arr, n):
    return [i for i, val in heapq.nlargest(n, enumerate(arr), key=lambda x: x[1])]

def process_recommendation(ind):
    recommendation = {}
    recommendation['name'] = rec['object_metadata']['name'][ind]
    recommendation['location'] = rec['object_metadata']['location'][ind]
    recommendation['rating'] = rec['object_metadata']['rating'][ind]
    recommendation['reviews'] = rec['object_metadata']['reviews'][ind]
    return recommendation

def recommend(hotel_id):
    user_list = rec['hotels_users'][hotel_id]
    usr_id = random.choice(user_list)
    usr_idx = rec['user_ids_dict'][usr_id]
    U, S, V_t = svds(rec['interaction_matrix'].astype(np.float32), k=20)
    SVD_r = np.dot(np.sqrt(np.diag(S)), V_t)
    usr_vector = np.dot(U[usr_idx, :], SVD_r)
    scaled_values = scale_values(usr_vector)
    top_indices = get_top_n_indices(scaled_values, num_indices)
    recommendation_list = []
    for ind in top_indices:
        recommendation_list.append(process_recommendation(ind))
    return recommendation_list
