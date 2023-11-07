import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class Content_Studio:
    def __init__(self):
        df = pd.read_csv("./data/Studios.csv", index_col="Id")
        self.df = df

    def recommend(self, target_id):
        target_genres = self.df.loc[target_id, :].values.reshape(1, -1)
        similarities = cosine_similarity(target_genres, self.df.values)
        similar_indices = similarities.argsort()[0][::-1]
        similar_ids = self.df.index[similar_indices].tolist()
        similar_scores = similarities[0][similar_indices].tolist()
        similar_id_score_pairs = list(zip(similar_ids, similar_scores))
        return similar_id_score_pairs

#cn = Content_Studio()
#print(cn.recommend(18679))