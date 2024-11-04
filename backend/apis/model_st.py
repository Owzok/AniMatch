import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from typing import List, Tuple, Optional

class Content_Meta:
    def __init__(self, csv_path: str = "./data/anime.csv"):
        self.df = self._preprocess_data(csv_path)

    def _preprocess_data(self, csv_path: str) -> pd.DataFrame:
        """
        Preprocess the data by dropping unnecessary columns and cleaning the text data.
        """
        df = pd.read_csv(csv_path)
        df.set_index("MAL_ID", inplace=True)
        df = df.iloc[:,:20]
        df.drop(['Japanese name', 'English name', 'Rating', 'Duration', 'Premiered', 'Aired'], axis=1, inplace=True)
        df2 = pd.get_dummies(df, columns=['Type', 'Source'])
        df2.drop(["Name", "Genres", "Producers", "Licensors", "Studios"], axis=1, inplace=True)
        df2 = df2[df2.Score != 'Unknown']
        df2 = df2[df2.Episodes != 'Unknown']
        df2.drop(["Ranked"], axis=1 ,inplace=True)
        df2 = df2.iloc[:,6:]
        return df2

    def recommend(self, target_id: int) -> List[Tuple[int, float]]:
        try:
            target_genres = self.df.loc[target_id, :].values.reshape(1, -1)
            similarities = cosine_similarity(target_genres, self.df.values)
            similar_indices = similarities.argsort()[0][::-1] # Exclude the first one (itself)
            similar_ids = self.df.index[similar_indices].tolist()
            similar_scores = similarities[0][similar_indices].tolist()
            similar_id_score_pairs = list(zip(similar_ids, similar_scores))
            return similar_id_score_pairs
        except KeyError:
            print(f"Anime with MAL_ID {target_id} not found in the dataset.")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

#mg = Content_Meta()
#print(mg.recommend(1)[0])