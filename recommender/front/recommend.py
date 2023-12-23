import pickle
from scipy.sparse.linalg import svds
import numpy as np
import heapq
import random

# number of recommendations
N = 10 

with open('recommender.pkl', 'rb') as f:
    rec = pickle.load(f)

def scale_SVD_values(values):
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
    U3, S3, Vt3 = svds(rec['interaction_matrix'].astype(np.float32), k=20)
    SVD_right3 = np.dot(np.sqrt(np.diag(S3)), Vt3)
    prod3 = np.dot(U3[usr_idx, :], SVD_right3)
    scaled_values3 = scale_SVD_values(prod3)
    print(np.argmax(scaled_values3))
    top_N_indices3 = get_top_n_indices(scaled_values3, N)
    recommendation_list = []
    for ind in top_N_indices3:
        recommendation_list.append(process_recommendation(ind))
    return recommendation_list
