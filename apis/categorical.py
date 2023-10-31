import numpy as np 
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_text(text):
    if isinstance(text, str):
        words = word_tokenize(text)
        
        cleaned_words = [re.sub('[^A-Za-z0-9]+', '', word) for word in words]
        
        stop_words = set(stopwords.words('english'))
        cleaned_words = [word for word in cleaned_words if word not in stop_words]
        
        # Join the cleaned words with a space
        processed_text = ' '.join(cleaned_words)
        return processed_text
    else:
        return text  # Return the input as is if it's not a string

class Content_Categorical:
    def __init__(self):
        cf = pd.read_csv("anime_with_synopsis.csv")
        cf.drop(["Score"], axis=1, inplace=True)
        cf['Genres'] = cf['Genres'].apply(lambda x: x.replace(",", "").lower())
        cf['sypnopsis'] = cf['sypnopsis'].apply(lambda x: str(x).replace(",", "").lower())
        cf['sypnopsis'] = cf['sypnopsis'].apply(preprocess_text)

        cf['tags'] = cf['Genres'] + cf['sypnopsis']
        cf.drop(['sypnopsis', 'Genres'], axis=1, inplace=True)
        self.cf = cf
        tfidf_vectorizer = TfidfVectorizer(max_features=20000, stop_words='english')
        tfidf_vectors = tfidf_vectorizer.fit_transform(cf['tags'])
        self.similarity = cosine_similarity(tfidf_vectors)
    
    def recommend(self, title):
        anime_id = self.cf[self.cf['Name'] == title]['MAL_ID'].values[0]  # Get MAL_ID

        if anime_id is not None:
            anime_index = self.cf[self.cf['MAL_ID'] == anime_id].index[0]
            distances = self.similarity[anime_index]
            anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#            for i in anime_list:
#                anime_name = self.cf.iloc[i[0]]['Name']
#                print(f'{anime_name}: {i[1]}')  # Print anime name and similarity score

            recommended_anime_data = [(self.cf.iloc[i[0]]['MAL_ID'], i[1]) for i in anime_list]

            return recommended_anime_data
        else:
            print("Anime not found in the dataset")
            return None