import heapq
import os
import pickle
import random

import numpy as np
from scipy.sparse.linalg import svds


class Recommender:
    # number of recommendations
    num_indices = 10

    def __init__(self):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'recommender.pkl')
        with open(file_path, 'rb') as f:
            self.rec = pickle.load(f)

    def scale_values(self, values):
        min_value = min(values)
        _values = [value - min_value for value in values]
        max_value = max(_values)
        _values = [value / max_value for value in _values]
        _values = [1 - value for value in _values]
        return _values

    def get_top_n_indices(self, arr, n):
        return [i for i, val in heapq.nlargest(n, enumerate(arr), key=lambda x: x[1])]

    def process_recommendation(self, ind):
        recommendation = {}
        recommendation['name'] = self.rec['object_metadata']['name'][ind]
        recommendation['location'] = self.rec['object_metadata']['location'][ind]
        recommendation['rating'] = self.rec['object_metadata']['rating'][ind]
        recommendation['reviews'] = self.rec['object_metadata']['reviews'][ind]
        return recommendation

    def recommend(self, hotel_id):
        # user selection
        user_list = self.rec['hotels_users'][hotel_id]
        usr_id = random.choice(user_list)
        usr_idx = self.rec['user_ids_dict'][usr_id]
        # truncated SVD
        U, S, V_t = svds(self.rec['interaction_matrix'].astype(np.float32), k=20)
        SVD_r = np.dot(np.sqrt(np.diag(S)), V_t)
        usr_vector = np.dot(U[usr_idx, :], SVD_r)
        # scaling, top selection
        scaled_values = self.scale_values(usr_vector)
        top_indices = self.get_top_n_indices(scaled_values, self.num_indices)

        recommendation_list = []
        for ind in top_indices:
            recommendation_list.append(self.process_recommendation(ind))
        return recommendation_list
