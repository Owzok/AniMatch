# --- Flask ---
from flask import Flask, request, jsonify
from model_content import ContentBasedRecommender
from colab import ColaborativeRecommender
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
from difflib import SequenceMatcher         # search title by name

import os
import concurrent.futures
from io import BytesIO
from bs4 import BeautifulSoup


app = Flask(__name__)
CORS(app) 
cb = ContentBasedRecommender()
cf = ColaborativeRecommender()

cwd = os.getcwd()
IMAGE_FOLDER = '../public/download/'
os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)
MAIN_PATH = "../public/download/profiles/"
RETURNABLE_PATH = "../download/profiles/"

try: 
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")

    #service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        #service=service,
        options=chrome_options
    )
except:
    print("Machine is not Windows, cannot do webscraping !")

SLEEP_TIME = 1

df = pd.read_csv("./data/data_anime_clean.csv", index_col="Id")
synopsis = pd.read_csv("./data/anime_with_synopsis.csv", index_col="MAL_ID")
data = pd.read_csv("./data/data4filter.csv")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def retrieve_id(title):
    if title is None:
        return jsonify({"error": "Invalid request. Make sure title are provided "}), 400

    df['r'] = df.apply(lambda x: similar(x.Name, title), axis=1)
    return df['r'].idxmax()

def do_filtering(data, min_score=1, max_score=10, min_episodes=1, max_episodes=10000, min_year=1970, max_year=2023):
    if max_episodes == 100:
        max_episodes = 10000
    return data[(data['Score'] >= min_score) & (data['Score'] <= max_score) & (data['Episodes'] >= min_episodes) & (data['Episodes'] <= max_episodes) & (data['Year'] >= min_year) & (data['Year'] <= max_year) & (data['Year'] >= min_year)]


def save_image(anime_id):
    full_url = MAIN_PATH+f"{anime_id}.jpg"
    returnable_url = RETURNABLE_PATH+f"{anime_id}.jpg"
    if os.path.isfile(full_url):
        print("si hay", anime_id)
        return (anime_id, returnable_url)
    else:
        print("no hay", anime_id)
        url = "https://myanimelist.net/anime/"
        response = requests.get(url+str(anime_id))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            div_tag = soup.find('div', {'class': 'leftside'})
            img_tag = div_tag.find('img') if div_tag else None
            if img_tag:
                img_url = img_tag['data-src']

                response = requests.get(img_url)
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                
                image.save(full_url)
                print(f"Image saved as {anime_id}.jpg")
                
                return (anime_id, returnable_url)
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return (response.status_code, None)

def get_lst_images(lst_recommend):
    imgs_anime = {}
    with concurrent.futures.ThreadPoolExecutor() as mainExecutor:
        future_execution = [mainExecutor.submit(save_image,
                                            anime)
                            for anime in lst_recommend]
        if future_execution is not None: 
            for future in concurrent.futures.as_completed(future_execution):
                resultado = future.result()
                if resultado is not None: 
                    imgs_anime[resultado[0]] = resultado[1]
    return imgs_anime

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

    data_new_user = pd.read_csv(f"../public/users/{username}.csv")
    nuevo_df, lst_anime, anime_id_ratings = cf.recommend(data_new_user, 10)

    #Hacer todos los filtros en nuevo_df

    anime_titles =nuevo_df["Title"].tolist()
    anime_id =nuevo_df.index

    anime_id = anime_id
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

    return jsonify({ "results": json_data })

@app.route('/anirec', methods=['POST'])
@cross_origin()
def get_anirec():
    data = request.json
    id = retrieve_id(data.get('title'))
    title = df.loc[id].Name

    if title is None:
        return jsonify({"error": "Invalid request. Make sure 'title' and 'k' are provided."}), 400

    recommendations = cb.recommend_ten(title)

    jsonifiable_data = [{'anime_id': int(anime_id), 'anime_image_url': anime_image_url} for anime_id, anime_image_url in recommendations]
    json_data = json.dumps(jsonifiable_data)

    return jsonify({"results": json_data})

def scroll_to_bottom():
    '''Scroll to the bottom of the page'''
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(7)

        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            element = driver.find_element(
                by=By.CSS_SELECTOR,
                value='.YstHxe input'
            )
            element.click()
            time.sleep(1)
        except:
            pass

        if new_height == last_height:
            break

        last_height = new_height

@app.route('/scrap_user', methods=['POST'])
def scrap_user():
    data = request.json
    username = data.get('username')

    url = f"https://myanimelist.net/animelist/{username}?status=7&order=4&order2=0"

    driver.get(url)
    scroll_to_bottom()
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
    df.to_csv(f"../public/users/{username}.csv", index=False)
    return json.dumps({"Status Code": 200})

@app.route('/get_malid', methods=['POST'])
@cross_origin()
def get_id():
    data = request.json
    title = data.get('title')
    if title is None:
        return jsonify({"error": "Invalid request. Make sure title are provided "}), 400

    df['r'] = df.apply(lambda x: similar(x.Name, title), axis=1)
    return jsonify({"id":str(df['r'].idxmax())})

@app.route('/get_info', methods=['POST'])
def get_info():
    data = request.json
    print(data)
    id = int(data.get('id'))
    #print("\n\n\n\n",id,"\n\n\n\n\n")

    def get_length_text(id):
        x = synopsis.loc[id].sypnopsis.split(".")
        m_len = 0
        f_text = []
        for i in range(len(x)):
            if m_len > 360:
                break
            m_len += len(x[i])
            f_text.append(x[i])
            #print(m_len)
        return " ".join(str(item) for item in f_text)    

    desc = get_length_text(id)
    fields = ['Name', 'Type', 'Episodes', 'Studios', 'Rating', 'Genres']
    filtered_data = df.loc[id, fields]
    result_dict = filtered_data.to_dict()
    result_dict['synopsis'] = desc
    return jsonify(result_dict)

@app.route('/scrape_image', methods=['POST'])
@cross_origin()
def scrape_image():
    data = request.json
    id = int(data.get('id'))
    
    search_query = df.loc[id].Name

    mal_id = data.get('id')
    #num_images = data.get('num_images')

    #if not search_query or num_images is None:
    if search_query is None and mal_id is None:
        return jsonify({"error": "Invalid request. Make sure 'search_query' and 'id' are provided."}), 400

    def download_google_images(search_query: str, mal_id: int):
        def save_image(image_url):
            response = requests.get(image_url)

            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image.save(f"../public/download/{id}.jpg")

                print(f"Image saved as {mal_id}.jpg")
                return 200
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                return response.status_code

        def save_base64(b64, title):
            try:
                base64_data = b64.split(',')[1]
                image_data = base64.b64decode(base64_data)
                image_stream = BytesIO(image_data)
                image = Image.open(image_stream)
                image.save(f'../public/download/{id}.jpg', 'JPEG')
                print(f"Image saved as {search_query}.jpg")
                image_stream.close()
            except:
                print("Bad Image")


        def scroll_to_bottom():
            '''Scroll to the bottom of the page
            '''
            last_height = driver.execute_script('return document.body.scrollHeight')
            while True:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

                new_height = driver.execute_script('return document.body.scrollHeight')
                try:
                    element = driver.find_element(
                        by=By.CSS_SELECTOR,
                        value='.YstHxe input'
                    )
                    element.click()
                    time.sleep(SLEEP_TIME)
                except:
                    pass

                if new_height == last_height:
                    break

                last_height = new_height

        url = 'https://images.google.com/'

        driver.get(
            url=url
        )

        box = driver.find_element(
            by=By.XPATH,
            value='//*[@id="APjFqb"]'
        )

        box.send_keys(search_query+" anime imagesize:1920x1080 filetype:jpg OR filetype:png")
        box.send_keys(Keys.ENTER)
        time.sleep(0.5)

        #scroll_to_bottom()
        #time.sleep(SLEEP_TIME)

        img_results = driver.find_elements(
            by=By.XPATH,
            value="//img[contains(@class,'rg_i Q4LuWd')]"
        )

        total_images = len(img_results)

        print(f'Total images - {total_images}')

        count = 0

        first_image = driver.find_element(
            by=By.XPATH,
            value='//img[contains(@class,"rg_i Q4LuWd")]'
        )

        # Extract the image source
        img_src = first_image.get_attribute("src")

        #print(f'First image - {first_image}')
        #print(f'Image source - {img_src}')

        for img_result in img_results:
            WebDriverWait(
                driver,
                    5
                ).until(
                    EC.element_to_be_clickable(
                        img_result
                    )
                )
            img_result.click()
                # Hasta aca entro, busco y dio click en la primera imagen
                #print("zzzz")
            #time.sleep(SLEEP_TIME)
            time.sleep(SLEEP_TIME)
                #time.sleep(100000)

            actual_imgs = driver.find_element(
                by=By.XPATH,
                value='//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
            )
                
            xpath = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
            wait = WebDriverWait(driver, 15)

            x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            #print(x.get_attribute("src"))
            img_url = x.get_attribute("src")
            if img_url[:5] == 'https':
                print("GG")
                
                if save_image(img_url) == 200:
                    return
                else:
                    continue

    try:
        #download_google_images(search_query, num_images)
        download_google_images(search_query, mal_id)
        #return jsonify({"message": f"Scraped and saved {num_images} images for query: {search_query}."})
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
    fetched_data_str = content.get('fetched_data', [])
    fetched_data = [ast.literal_eval(item) for item in fetched_data_str]
    df = pd.DataFrame(fetched_data, columns=['Id', 'model_score'])

    final_df = pd.merge(df, data, on="Id")

    filtered_data = do_filtering(final_df, min_score=min_score, max_score=max_score, min_episodes=min_episodes, max_episodes=max_episodes, min_year=min_year, max_year=max_year)

    result_df = pd.DataFrame(filtered_data)
    print(result_df)
    print(result_df['Id'].values)
    # You can return the result as JSON
    return jsonify(result_df['Id'][:10].values.tolist())

if __name__ == '__main__':
    app.run(debug=True)