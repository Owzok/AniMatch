import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Content_Meta:
    def __init__(self):
        df = pd.read_csv("./data/anime.csv")
        df.set_index("MAL_ID", inplace=True)
        df = df.iloc[:,:20]
        df.drop(['Japanese name', 'English name', 'Rating', 'Duration', 'Premiered', 'Aired'], axis=1, inplace=True)
        df2 = pd.get_dummies(df, columns=['Type', 'Source'])
        df2.drop(["Name", "Genres", "Producers", "Licensors", "Studios"], axis=1, inplace=True)
        df2 = df2[df2.Score != 'Unknown']
        df2 = df2[df2.Episodes != 'Unknown']
        df2.drop(["Ranked"], axis=1 ,inplace=True)
        df2 = df2.iloc[:,6:]
        self.df = df2

    def recommend(self, target_id):
        target_genres = self.df.loc[target_id, :].values.reshape(1, -1)
        similarities = cosine_similarity(target_genres, self.df.values)
        similar_indices = similarities.argsort()[0][::-1]
        similar_ids = self.df.index[similar_indices].tolist()
        similar_scores = similarities[0][similar_indices].tolist()
        similar_id_score_pairs = list(zip(similar_ids, similar_scores))
        return similar_id_score_pairs

#mg = Content_Meta()
#print(mg.recommend(1))