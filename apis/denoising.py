import pandas as pd
import pickle
import numpy as np
import tensorflow as tf

MODEL = "autoencoder"

def custom_loss(y_true, y_pred):
    weights = tf.where(tf.equal(y_true, 0), 0.1, 1.0)
    loss = tf.reduce_sum(tf.square(y_true - y_pred) * weights) / tf.reduce_sum(weights)
    return loss

def self_standarize_array(array):
    for idx in range(array.shape[0]):
        value = array[idx, 0]
        if value != 0:
            min_value = array[:, 0].min()
            max_value = array[:, 0].max()
            array[idx, 0] = 0 if value == 0 else (value - min_value) / (max_value - min_value) * 2 - 1
    return array

class DenoisingAutoEncoder:
    def __init__(self):
        self.model = tf.keras.models.load_model(f"./models/{MODEL}.h5", custom_objects={'custom_loss': custom_loss})
        self.df_ids = pd.read_csv("./data/10k.csv")
        print("model loaded !")

    def recommend(self, data_user, k_to_recommend=10):
        print("Input data_user:")
        print(data_user[:10])

        filtered_ratings = data_user[data_user['anime_id'].isin(self.df_ids['Id'])]
        print("Filtered ratings:")
        print(filtered_ratings[:10])

        filtered_ratings = pd.merge(self.df_ids, filtered_ratings, how='left', left_on='Id', right_on='anime_id')
        print("Merged filtered ratings:")
        print(filtered_ratings[:10])

        filtered_ratings = filtered_ratings['rating'].fillna(0).values.reshape(-1, 1)
        print("Reshaped and filled ratings:")
        print(filtered_ratings[:10])

        filtered_ratings = self_standarize_array(filtered_ratings).reshape(1, 4697)
        print("Standardized ratings:")
        print(filtered_ratings[:10])

        predictions = self.model.predict(filtered_ratings)
        print("Predictions:")
        print(predictions[:10])

        sorted_ids = [(index, value) for index, value in enumerate(predictions[0])]
        sorted_ids = sorted(sorted_ids, key=lambda x: x[1], reverse=True)
        sorted_ids = [(index, value) for index, value in sorted_ids if self.df_ids.iloc[index]['Id'] not in data_user['anime_id'].values]

        print("Sorted and filtered predictions:")
        print(sorted_ids[:10])

        top_k_indices = [index for index, _ in sorted_ids]
        corresponding_ids = self.df_ids.iloc[top_k_indices]
        final = []
        ids = corresponding_ids['Id'].values
        for i in range(len(sorted_ids)):
            final.append((ids[i], sorted_ids[i][1]))

        print("Final recommendations:")
        print(final[:10])

        return final

#dae = DenoisingAutoEncoder()
#print(dae.recommend(pd.read_csv("../public/users/Owzok.csv"), 10))