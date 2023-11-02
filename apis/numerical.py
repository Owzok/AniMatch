import numpy as np 
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

class Content_Numerical:
    def __init__(self):
        df = pd.read_csv("anime.csv")
        df.set_index("MAL_ID", inplace=True)
        df = df.iloc[:,:20]
        df.drop(['Japanese name', 'English name', 'Rating', 'Duration', 'Premiered', 'Aired'], axis=1, inplace=True)
        self.df = df
        df2 = pd.get_dummies(df, columns=['Type', 'Source'])
        df2.drop(["Name", "Genres", "Producers", "Licensors", "Studios"], axis=1, inplace=True)
        df2 = df2[df2.Score != 'Unknown']
        df2 = df2[df2.Episodes != 'Unknown']
        df2.drop(["Ranked"], axis=1 ,inplace=True)
        scaler = MinMaxScaler()
        df3 = scaler.fit_transform(df2)
        df3 = pd.DataFrame(df3, columns=df2.columns, index=df2.index)
        df3.drop(["Source_Digital manga", "Source_Other", "Source_Picture book", "Source_Radio", "Source_Unknown", "Type_Unknown", "Watching"], axis=1, inplace=True)
        self.df3 = df3

    def recommend(self, n_id, display=False):
        anime_1_features = self.df3.loc[n_id].values.reshape(1, -1)
        similarities = cosine_similarity(self.df3, anime_1_features)

        similarities = pd.Series(similarities.flatten(), index=self.df3.index)

        recommended_anime = similarities.sort_values(ascending=False)

        #print(f"Top Recommended Anime for MAL_ID {self.df.loc[n_id]['Name']}:\n")
        #print(recommended_anime.head(10))  # Print the top 10 recommendations

        #for i in recommended_anime.iloc[:10].index:
        #    print(self.df.loc[i]['Name'])

        return [(index, recommended_anime[index]) for index in recommended_anime.index]
    
#cn = Content_Numerical()
#cn.recommend(223)