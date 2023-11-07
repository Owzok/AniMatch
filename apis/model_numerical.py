import numpy as np 
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

def scale_rating(rating: int) -> float:
    rating = float(rating)
    if rating >= 9:
        return 10
    if rating >= 8:
        return 8
    if rating >= 7:
        return 5
    if rating >= 6:
        return -1
    else:
        return -10
    raise ValueError("Invalid rating: {}".format(rating))

class Content_Numerical:
    def __init__(self):
        df = pd.read_csv("./data/anime.csv")
        df.set_index("MAL_ID", inplace=True)
        df = df.iloc[:,:20]
        df.drop(['Japanese name', 'English name', 'Rating', 'Duration', 'Premiered', 'Aired'], axis=1, inplace=True)
        self.df = df
        df2 = df.copy()
        df2.drop(["Name", "Genres", "Producers", "Licensors", "Studios", "Type", "Source", "Watching", "Favorites"], axis=1, inplace=True)
        df2 = df2[df2.Score != 'Unknown']
        df2 = df2[df2.Episodes != 'Unknown']
        df2.drop(["Ranked"], axis=1 ,inplace=True)
        df2['Score'] = df2['Score'].apply(scale_rating)
        score_col = df2['Score']
        scaler = MinMaxScaler()
        df3 = scaler.fit_transform(df2)
        df3 = pd.DataFrame(df3, columns=df2.columns, index=df2.index)
        df3['Score'] = score_col
        self.df3 = df3

    def recommend(self, n_id):
        #print(self.df3)

        anime_1_features = self.df3.loc[n_id].values.reshape(1, -1)
        similarities = cosine_similarity(self.df3, anime_1_features)

        similarities = pd.Series(similarities.flatten(), index=self.df3.index)

        recommended_anime = similarities.sort_values(ascending=False)

        #print(f"Top Recommended Anime for MAL_ID {self.df.loc[n_id]['Name']}:\n")
        #print(recommended_anime.head(10))  # Print the top 10 recommendations

        #for i in recommended_anime.iloc[:10].index:
        #    print(self.df.loc[i]['Name'])

        return [(index, (recommended_anime[index] - 0.999)*1000) for index in recommended_anime.index]
    
#cn = Content_Numerical()
#cn.recommend(1)