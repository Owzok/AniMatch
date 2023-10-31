from numerical import Content_Numerical
from categorical import Content_Categorical
import pandas as pd

class ContentBasedRecommender:
    def __init__(self):
        self.df = pd.read_csv("anime.csv")
        self.cc = Content_Categorical()
        self.cn = Content_Numerical()

    def get_id_from_title(self, title):
        anime = self.df[self.df['Name'] == title]
        if not anime.empty:
            return anime['MAL_ID'].values[0]
        return None

    def recommend(self, title, k):
        n_id = self.get_id_from_title(title)
        if n_id is None:
            return []  # Anime not found

        cate = self.cc.recommend(title)
        num = self.cn.recommend(n_id)

        combined = {}
        for anime_id, score in num:
            combined[anime_id] = 0.8 * score

        for anime_id, score in cate:
            if anime_id in combined:
                combined[anime_id] += 0.001 * score
            else:
                combined[anime_id] = 0.001 * score

        sorted_combined = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:k]

        recs = []

        for anime_id, _ in sorted_combined:
            anime_name = self.df[self.df['MAL_ID'] == anime_id]['Name'].values[0]
            recs.append(anime_name)

        return recs