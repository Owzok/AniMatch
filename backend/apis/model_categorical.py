import numpy as np 
import pandas as pd

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from typing import List, Tuple, Optional

def preprocess_text(text: str) -> str:
    """
    Preprocesses the input text by removing non-alphanumeric characters and stopwords, and lowercases it.

    Input: `string text`

    Output: `string processed_text` lowercased, without stop words and non alphanumeric characters
    """
    
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    
    # Remove non-alphanumeric characters
    text = re.sub('[^A-Za-z0-9]+', '', text.lower())


    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in word_tokenize(text) if word not in stop_words]

    # Join the cleaned words with a space
    processed_text = ' '.join(words)

    return processed_text

class Content_Categorical:
    def __init__(self, csv_path: str = "./data/anime_with_synopsis.csv"):
        # Load the dataset with synopsis
        self.cf = pd.read_csv(csv_path)
        
        self._preprocess_data()

        self._create_tfidf_similarityvectors()

    def _preprocess_data(self):
        """
        Preprocess the data by dropping unnecessary columns and cleaning the text data.
        """

        # Drop unnecessary columns and preprocess the text (Genres and Synopsis)
        self.cf.drop(["Score"], axis=1, inplace=True)
        self.cf['Genres'] = self.cf['Genres'].str.replace(",", "").str.lower()
        self.cf['sypnopsis'] = self.cf['sypnopsis'].astype(str).apply(preprocess_text)
        self.cf['tags'] = self.cf['Genres'] + self.cf['sypnopsis']
        self.cf.drop(['sypnopsis', 'Genres'], axis=1, inplace=True)

    def _create_tfidf_similarityvectors(self):
        """
        Create the TF-IDF vectors and calculate the cosine similarity between the vectors.
        """

        # Create a TfidfVectorizer object to transform the text into a vector
        tfidf_vectorizer = TfidfVectorizer(max_features=20000, stop_words='english')
        tfidf_vectors = tfidf_vectorizer.fit_transform(self.cf['tags'])

        # Calculate the cosine similarity between the vectors and store it in a variable
        self.similarity = cosine_similarity(tfidf_vectors)
    
    def recommend(self, title: str) -> List[Tuple[int, float]]:
        """
        Recommends anime based on the input title.

        Input: `string title`

        Output: `list recommended_anime_data` with the MAL_ID and similarity score. Or None if the anime is not found.
        """

        try:
            anime = self.cf[self.cf['Name'] == title]

            if anime.empty:
                print(f"Anime {title} not found in the dataset")
                return None

            anime_index = anime.index[0]
            distances = self.similarity[anime_index]
            anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    
            recommended_anime_data = [(int(self.cf.iloc[i[0]]['MAL_ID']), float(similarity)) for i, similarity in anime_list]

            return recommended_anime_data
        except Exception as e:
            print(f"An error ocurred: {e}")
            return None
        
#cc = Content_Categorical()
#print(cc.recommend("Cowboy Bebop"))