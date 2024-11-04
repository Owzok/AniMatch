# --- Utils ---
from utils.helpers import (
    similar, 
    retrieve_id, 
    do_filtering, 
    scroll_to_bottom, 
    get_length_text, 
    download_google_images,
    get_lst_images,
    startup_driver
)

# --- Flask ---
from flask import Flask, request, jsonify
from model_content import ContentBasedRecommender
from colab import ColaborativeRecommender
from denoising import DenoisingAutoEncoder
from flask_cors import CORS, cross_origin

import ast 
import json
import time                                 # time.sleep
import base64                               # save image in base 64
from io import BytesIO                      # save image
import re                                   # regex 
import os                                   # system operations

# --- Webscrapping ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
import requests                             # webscrapping
from PIL import Image                       # save image from google
import pandas as pd                         # read dataframe

IMAGE_FOLDER = '../../frontend/public/download/' 
SLEEP_TIME = 1

app = Flask(__name__)
CORS(app)

cb = ContentBasedRecommender()
cf = ColaborativeRecommender()
dcae = DenoisingAutoEncoder()

cwd = os.getcwd()

os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)

#TODO: Optimize the way we do this
df_anime_clean = pd.read_csv("./data/data_anime_clean.csv", index_col="Id")
df_anime_synopsis = pd.read_csv("./data/anime_with_synopsis.csv", index_col="MAL_ID")
data = pd.read_csv("./data/m_data4filter.csv")


@app.route('/profile_pics', methods=['POST'])
def get_pfps():
    data = request.json
    ids = data.get('ids')
    get_lst_images(ids)
    return jsonify({ "results": "Success" })

@app.route('/recommend', methods=['POST'])
@cross_origin()
def get_recommendations():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "<animatch> Invalid request. Make sure 'username' is provided."})

    data_new_user = pd.read_csv(f"../../frontend/public/users/{username}.csv")

    #TODO: For some reason, code now dies if it tries to train new user.
    nuevo_df, lst_anime, anime_id_ratings = cf.recommend(data_new_user, 10)

    #Hacer todos los filtros en nuevo_df
    anime_titles =nuevo_df["Title"].tolist()
    anime_id = nuevo_df.index

    anime_titles = anime_titles
    anime_id_ratings = anime_id_ratings
    lst_id_url = []
    lst_url = get_lst_images(anime_id[:10])

    for x in range(10):
        animeid = anime_id[x]
        lst_id_url.append((animeid, lst_url[animeid], str(anime_id_ratings[x])))
    for x in (range(len(anime_id_ratings[10:]))):
        animeid = anime_id[0]
        lst_id_url.append((animeid, lst_url[animeid], str(anime_id_ratings[10 + x])))
    jsonifiable_data = [{'anime_id': int(anime_id), 'anime_image_url': anime_image_url, 'score': score} for anime_id, anime_image_url, score in lst_id_url]
    json_data = json.dumps(jsonifiable_data)
    print(json_data)
    return jsonify({ "results": json_data })

@app.route("/interec", methods=['POST'])
def get_inter_rec():
    data = request.json
    user_ids = data.get('user_ids')
    anime_ids = list(map(int, data.get('anime_ids')))  
    ratings = list(map(int, data.get('ratings')))  

    if not anime_ids or not ratings or len(ratings) != len(anime_ids):
        return jsonify({"error": "<animatch> Invalid request. Make sure 'username' is provided."})
    
    data_inter_user = pd.DataFrame({
        'user_id': [141532434 for i in range(len(anime_ids))],
        'anime_id': anime_ids,
        'rating': ratings
    })

    print("Data for /interec:")
    print(data_inter_user)

    anime_id_ratings = dcae.recommend(data_inter_user)
    print("GAAAAAAAA /interec")
    print(anime_id_ratings[:20])

    lst_id_url = []
    anime_id = [id for id, value in anime_id_ratings]
    lst_url = get_lst_images(anime_id[:10])

    for x in range(10):
        animeid = anime_id[x]
        lst_id_url.append((animeid, lst_url[animeid], str(anime_id_ratings[x])))

    for x in (range(len(anime_id_ratings[10:]))):
        animeid = anime_id[0]
        lst_id_url.append((animeid, lst_url[animeid], str(anime_id_ratings[10 + x])))

    jsonifiable_data = [{'anime_id': int(anime_id), 'anime_image_url': anime_image_url, 'score': score} for anime_id, anime_image_url, score in lst_id_url]
    json_data = json.dumps(jsonifiable_data)

    return jsonify({ "results": json_data })

@app.route('/recommendae', methods=['POST'])
@cross_origin()
def get_anirec_dcae():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "<animatch> Invalid request. Make sure 'username' is provided."})

    data_new_user = pd.read_csv(f"../../frontend/public/users/{username}.csv")

    print("Data for /recommendae:")
    print(data_new_user)

    anime_id_ratings = dcae.recommend(data_new_user)
    print("GAAAAAAAA /recommendae")
    print(anime_id_ratings[:20])

    lst_id_url = []
    anime_id = [id for id, value in anime_id_ratings]
    lst_url = get_lst_images(anime_id[:10])

    for x in range(10):
        animeid = anime_id[x]
        lst_id_url.append((animeid, lst_url[animeid], str(anime_id_ratings[x])))

    for x in (range(len(anime_id_ratings[10:]))):
        animeid = anime_id[0]
        lst_id_url.append((animeid, lst_url[animeid], str(anime_id_ratings[10 + x])))

    jsonifiable_data = [{'anime_id': int(anime_id), 'anime_image_url': anime_image_url, 'score': score} for anime_id, anime_image_url, score in lst_id_url]
    json_data = json.dumps(jsonifiable_data)

    return jsonify({ "results": json_data })

@app.route('/anirec', methods=['POST'])
@cross_origin()
def get_anirec():
    data = request.json
    id = retrieve_id(data.get('title'), df_anime_clean)

    if id is None:
        return jsonify({"error": "Invalid request. Make sure title are provided "}), 400

    title = df_anime_clean.loc[id].Name

    if title is None:
        return jsonify({"error": "Invalid request. Make sure 'title' and 'k' are provided."}), 400

    recommendations = cb.recommend(title)

    lst_id_url = []
    anime_id = [id for id, value in recommendations]
    lst_url = get_lst_images(anime_id[:10])

    for x in range(10):
        animeid = anime_id[x]
        lst_id_url.append((animeid, lst_url[animeid], str(recommendations[x])))

    for x in (range(len(recommendations[10:]))):
        animeid = anime_id[0]
        lst_id_url.append((animeid, lst_url[animeid], str(recommendations[10 + x])))

    jsonifiable_data = [{'anime_id': int(anime_id), 'anime_image_url': anime_image_url, 'score': score} for anime_id, anime_image_url, score in lst_id_url]
    json_data = json.dumps(jsonifiable_data)

    return jsonify({"results": json_data})

@app.route('/scrap_user', methods=['POST'])
def scrap_user():
    data = request.json
    username = data.get('username')

    url = f"https://myanimelist.net/animelist/{username}?status=7&order=4&order2=0"

    driver = startup_driver()
    driver.get(url)
    scroll_to_bottom(driver)
    time.sleep(1)
    
    list_items = driver.find_elements(By.CLASS_NAME, "list-item")
    anime_list = []
    for item in list_items:
        m_anime = {}
        link = item.find_element(By.CLASS_NAME, "link")
        href = link.get_attribute("href")
        score_label = item.find_element(By.CLASS_NAME, "score-label").text
        m_anime['user_id'] = 786
        m_anime['anime_id'] = href.split("/")[4]
        m_anime['rating'] = score_label
        if score_label != "-":
            anime_list.append(m_anime)
    df = pd.DataFrame(anime_list)
    df.to_csv(f"../../frontend/public/users/{username}.csv", index=False)
    return json.dumps({"Status Code": 200})

@app.route('/get_malid', methods=['POST'])
@cross_origin()
def get_id():
    data = request.json
    title = data.get('title')
    if title is None:
        return jsonify({"error": "Invalid request. Make sure title are provided "}), 400

    df_anime_clean['r'] = df_anime_clean.apply(lambda x: similar(x.Name, title), axis=1)
    return jsonify({"id":str(df_anime_clean['r'].idxmax())})

@app.route('/get_info', methods=['POST'])
def get_info():
    data = request.json
    #print(data)
    id = int(data.get('id'))
    
    try:
        desc = get_length_text(id, df_anime_synopsis)
        title = df_anime_synopsis["Name"].loc[id]
    except Exception as e:
        desc = "Description not found"
        title = ""
    
    if title:
        fields = ['Type', 'Episodes', 'Score', 'Members', 'Ranked', 'Genres']
    else:
        fields = ['Name', 'Type', 'Episodes', 'Score', 'Members' ,'Ranked', 'Genres']

    try:
        filtered_data = df_anime_clean.loc[id, fields]
        result_dict = filtered_data.to_dict()
    except Exception as e:
        result_dict = {"Name": "Not found", "Type": "", "Episodes": "-", "Score": "-",
                       "Members": "-", "Genres": "Not found"}
    if title:
        result_dict["Name"] = title
    result_dict['synopsis'] = desc
    return jsonify(result_dict)

@app.route('/scrape_image', methods=['POST'])
@cross_origin()
def scrape_image():
    data = request.json
    id = int(data.get('id'))
    
    search_query = df_anime_clean.loc[id].Name

    mal_id = data.get('id')
    #num_images = data.get('num_images')

    #if not search_query or num_images is None:
    if search_query is None and mal_id is None:
        return jsonify({"error": "Invalid request. Make sure 'search_query' and 'id' are provided."}), 400

    try:
        driver = startup_driver()
        download_google_images(search_query, mal_id, driver,IMAGE_FOLDER)
        return jsonify({"success": True,
            "message": f"scrapped Image for query: {search_query}."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/filter', methods=['POST'])
def filter_data():
    content = request.json

    min_score = int(content.get('min_score', 1))
    max_score = int(content.get('max_score', 10))
    min_episodes = int(content.get('min_episodes', 1))
    max_episodes = int(content.get('max_episodes', 10000))
    min_year = int(content.get('min_year', 1970))
    max_year = int(content.get('max_year', 2023))
    prequels = int(content.get('prequel', 0))
    mature = int(content.get('mature', 0))

    fetched_data_str = content.get('fetched_data', [])
    fetched_data = [ast.literal_eval(item) for item in fetched_data_str]
    df = pd.DataFrame(fetched_data, columns=['Id', 'model_score'])
    final_df = pd.merge(df, data, on="Id")

    filtered_data = do_filtering(final_df, min_score=min_score, max_score=max_score, min_episodes=min_episodes, max_episodes=max_episodes, min_year=min_year, max_year=max_year, prequels=prequels, mature=mature)

    result_df = pd.DataFrame(filtered_data)
    #print(result_df)
    #print(result_df['Id'].values)
    # You can return the result as JSON
    return jsonify(result_df['Id'].values.tolist())

if __name__ == '__main__':
    app.run(debug=True)