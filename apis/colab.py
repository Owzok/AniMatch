import pandas as pd
import pickle
import numpy as np

import requests
from bs4 import BeautifulSoup
from IPython.display import Image, display, HTML

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import io

from lightfm import LightFM
import pandas as pd
from scipy import sparse
from lightfm.data import Dataset
import time 
NUM_COMPONENTS = 30
MODEL_LOSS = "warp"

"""
TO DO:
- add second model to AB Test al momento de hibridizar
- pruebas brindando animes en los que no esten en el dataset de train mappeado para ver que no den error
- explicar operaciones con embeds
- pruebas con perfiles de usuario que de mart
- adaptador de data para que nos den anime y rating, y ya le asignemos un ID al user y saquemos ids de animes


- HIBRYDIZATION! (tomar en cuenta que cuando no hayan animes que detecte el colaborative
                    podria ser que el content based lo pueda recomendar)
"""

class ColaborativeRecommender:
    def __init__(self):
        with open("./model_"+MODEL_LOSS+"_1.pkl", 'rb') as model_file:
            self.model = pickle.load(model_file)
        with open("./dataset_save.pkl", 'rb') as dataset_file:
            self.df = pickle.load(dataset_file)

        self.map_animes = self.df.mapping()[2]
        self.inv_dict = {v: k for k, v in self.map_animes.items()}

        self.user_biases = self.model.get_user_representations()[0]
        self.user_embeddings = self.model.get_user_representations()[1]
        self.item_biases = self.model.get_item_representations()[0]
        self.item_embeddings = self.model.get_item_representations()[1]
        self.anime_titles = pd.read_csv("./anime_titles.csv")

    def get_anime_mapped(self, id_to_map):
        return self.map_animes.get(id_to_map, None)

    def get_anime_originalID(self, id_to_inverse):
        return self.inv_dict.get(id_to_inverse, None)

    #Para correr y ver imagenes de manera rapida
    def get_lst_images(self, lst_recommend):
        url = "https://myanimelist.net/anime/"
        lst_images = []
        for anime in lst_recommend:
            response = requests.get(url+str(anime))
            soup = BeautifulSoup(response.text, 'html.parser')
            div_tag = soup.find('div', {'class': 'leftside'})
            img_tag = div_tag.find('img') if div_tag else None
            if img_tag:
                image_url = img_tag['data-src']
                lst_images.append(image_url)
        
        return lst_images

    def try_outs(self, lst_images, lst_recommend):
        num_images = len(lst_images)
        images_per_row = 5
        num_rows = (num_images + images_per_row - 1) // images_per_row

        fig, axs = plt.subplots(num_rows, images_per_row, figsize=(20, 8))
        fig.subplots_adjust(wspace=0.4, hspace=0.4)

        for ax, (img_url, anime_id) in zip(axs.ravel(), zip(lst_images, lst_recommend)):
            image_url = img_url
            
            image_response = requests.get(image_url)
            image_data = image_response.content
            
            image = Image.open(io.BytesIO(image_data))
            img_array = np.array(image)
            
            ax.imshow(img_array)
            ax.axis('off')

        for i in range(num_images, num_rows * images_per_row):
            fig.delaxes(axs.ravel()[i])
                
        plt.tight_layout()
        plt.show()

    def new_user_model(self, data_new_user):
        dataset_new = Dataset()
        dataset_new.fit((data_new_user["user_id"].iloc[x] for x in range(len(data_new_user))),(data_new_user["anime_id"].iloc[x] for x in range(len(data_new_user))))
        (interactions, weights) = dataset_new.build_interactions(((data_new_user["user_id"].iloc[x], data_new_user["anime_id"].iloc[x]) for x in range(len(data_new_user))))
        modelo = LightFM(no_components = NUM_COMPONENTS, learning_rate=0.05, loss=MODEL_LOSS, random_state=27)

        return modelo, interactions, weights     
    
    def train_new_user(self, modelo_new, interactions_new, epochs=10):
        return modelo_new.fit(interactions_new, epochs=epochs)
    
    def generate_map_watched(self, data_new):
        lst_watched =[]
        for id, info in data_new.iterrows():
            anime_mapped = self.get_anime_mapped(info["anime_id"])
            if anime_mapped != None:
                lst_watched.append((anime_mapped, info["rating"]))
        lst_watched = sorted(lst_watched, key=lambda v: v[0])
        map_watched = dict(lst_watched)
        return map_watched

    def generate_embeds(self, modelo_new, map_watched):
        lst_embed = [map_watched.get(x,0) for x in range(self.item_embeddings.shape[0])]
        lst_embed = np.array(lst_embed)

        new_user_embedding = modelo_new.get_user_representations()[1]
        new_user_embedding_with_biases = new_user_embedding + modelo_new.get_user_representations()[0]

        #Proyectar en espacio latente
        projected_user_embedding = new_user_embedding_with_biases + np.dot(lst_embed, self.item_embeddings)

        return projected_user_embedding

    def predict_N_best_recommendations(self, map_watched, projected_user_embedding, N=10):
        predicted_ratings = np.dot(projected_user_embedding, self.item_embeddings.T) + self.item_biases
        predicted_ratings = predicted_ratings[0]
        top_N_indices = np.argsort(predicted_ratings)[::-1]
    
        lst_top_recommendations = []
        lst_animes_ratings = []
        for id, rating in zip(top_N_indices, predicted_ratings[top_N_indices]):
            watched = map_watched.get(id, None)
            if watched == None:
                title_original = self.anime_titles[self.anime_titles["Id"] == self.get_anime_originalID(id)]
                if len(title_original):
                    lst_top_recommendations.append(self.get_anime_originalID(id))
                    lst_animes_ratings.append((self.get_anime_originalID(id), rating))
        return lst_top_recommendations[:N], lst_animes_ratings[:N]

    def recommend(self, data_new_user, K_to_recommend=10):
        modelo_new, interactions_new, weights_new = self.new_user_model(data_new_user)
        modelo_new = self.train_new_user(modelo_new, interactions_new)

        map_watched = self.generate_map_watched(data_new_user)

        projected_user_embedding = self.generate_embeds(modelo_new, map_watched)

        lst_top_recommendations, lst_animes_ratings = self.predict_N_best_recommendations(map_watched, projected_user_embedding, K_to_recommend)

        #self.try_outs(self.get_lst_images(lst_top_recommendations), lst_top_recommendations)
        ids_en_df = self.anime_titles[self.anime_titles['Id'].isin(lst_top_recommendations)]
        nuevo_df =  pd.DataFrame(ids_en_df, columns=['Id', "Title"]).set_index('Id').reindex(lst_top_recommendations)
        anime_titles =nuevo_df["Title"].tolist()
        anime_id =nuevo_df.index

        lst_id_url = []
        lst_url = self.get_lst_images(anime_id)
        for x in range(len(anime_id)):
            lst_id_url.append((anime_id[x], lst_url[x]))

        return anime_titles, lst_animes_ratings, lst_id_url
    
cl = ColaborativeRecommender()
data_new_user = pd.read_csv("./new_user.csv")
titles, id_ratings, lst_id_url = cl.recommend(data_new_user, 10)

#print(id_ratings)

for elem in range(len(id_ratings)):
    print("Anime: ", titles[elem])
    #print("con score ", id_ratings[elem][1])

print(lst_id_url)
