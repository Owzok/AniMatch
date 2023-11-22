from model_numerical import Content_Numerical
from model_categorical import Content_Categorical
from model_genres import Content_Genre
from model_studio import Content_Studio
from model_st import Content_Meta
from bs4 import BeautifulSoup
import pandas as pd
import requests

class ContentBasedRecommender:
    def __init__(self):
        self.df = pd.read_csv("./data/anime.csv")
        self.cc = Content_Categorical()
        self.cn = Content_Numerical()
        self.gn = Content_Genre()
        self.cm = Content_Meta()
        self.cs = Content_Studio()

    def get_id_from_title(self, title):
        anime = self.df[self.df['Name'] == title]
        if not anime.empty:
            return anime['MAL_ID'].values[0]
        return None

    def get_lst_images(self, lst_recommend):
        print("retrieving images")
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

    def recommend_ten(self, title):
        n_id = self.get_id_from_title(title)

        cate = self.cc.recommend(title)
        num = self.cn.recommend(n_id)
        gen = self.gn.recommend(n_id)
        meta = self.cm.recommend(n_id)
        stud = self.cs.recommend(n_id)

        combined = {}
        
        for anime_id, score in num:
            combined[anime_id] = 0.7 * score

        for anime_id, score in cate:
            if anime_id in combined:
                combined[anime_id] += 0.1 * score
        
        for anime_id, score in gen:
            if anime_id in combined:
                combined[anime_id] += 0.15 * score

        for anime_id, score in meta:
            if anime_id in combined:
                combined[anime_id] += 0.1 * score

        for anime_id, score in stud:
            if anime_id in combined:
                combined[anime_id] += 0.05 * score

        sorted_combined = sorted(combined.items(), key=lambda x: x[1], reverse=True)[1:11]

        lst_id_url = []
        ids = [x[0] for x in sorted_combined]
        lst_url = self.get_lst_images(ids)
        #print(ids)
        #print(lst_url)
        for x in range(10):
            lst_id_url.append((ids[x], lst_url[x]))

        return lst_id_url        

    def recommend(self, title, k):
        n_id = self.get_id_from_title(title)
        if n_id is None:
            return []  # Anime not found

        cate = self.cc.recommend(title)
        num = self.cn.recommend(n_id)
        gen = self.gn.recommend(n_id)
        meta = self.cm.recommend(n_id)
        stud = self.cs.recommend(n_id)

        combined = {}
        
        for anime_id, score in num:
            combined[anime_id] = 0.7 * score

        for anime_id, score in cate:
            if anime_id in combined:
                combined[anime_id] += 0.1 * score
        
        for anime_id, score in gen:
            if anime_id in combined:
                combined[anime_id] += 0.15 * score

        for anime_id, score in meta:
            if anime_id in combined:
                combined[anime_id] += 0.1 * score

        for anime_id, score in stud:
            if anime_id in combined:
                combined[anime_id] += 0.05 * score

        sorted_combined = sorted(combined.items(), key=lambda x: x[1], reverse=True)[1:]
        return sorted_combined
        #print(sorted_combined)
        recs = []

        for anime_id, _ in sorted_combined:
            anime_name = self.df[self.df['MAL_ID'] == anime_id]['Name'].values[0]
            recs.append(anime_name)

            #print(f"---{anime_name}---")

            #for sanime_id, score in num:
            #    if sanime_id == anime_id:
            #        print("Numerical", score)
            #for sanime_id, score in cate:
            #    if sanime_id == anime_id:
            #        print("Categorical",score)
            #for sanime_id, score in gen:
            #    if sanime_id == anime_id:
            #        print("Genre",score)
            #for sanime_id, score in meta:
            #    if sanime_id == anime_id:
            #        print("Metadata",score)
            #for sanime_id, score in stud:
            #    if sanime_id == anime_id:
            #        print("Studio",score)

        return recs
    
#cb = ContentBasedRecommender()
#print(cb.recommend_ten("Bungou Stray Dogs"))