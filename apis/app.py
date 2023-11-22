# --- Flask ---
from flask import Flask, request, jsonify
from model_content import ContentBasedRecommender
from colab import ColaborativeRecommender
from flask_cors import CORS, cross_origin

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

app = Flask(__name__)
CORS(app) 
#cb = ContentBasedRecommender()
cf = ColaborativeRecommender()

cwd = os.getcwd()
IMAGE_FOLDER = '../public/download/'
os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)

try: 
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
except:
    print("Machine is not Windows, cannot do webscraping !")

SLEEP_TIME = 1

df = pd.read_csv("./data/anime.csv", index_col="MAL_ID")
synopsis = pd.read_csv("./data/anime_with_synopsis.csv", index_col="MAL_ID")
data_new_user = pd.read_csv("./data/user_tests/andre.csv")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.route('/recommend', methods=['POST'])
@cross_origin()
def get_recommendations():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "<animatch> Invalid request. Make sure 'username' is provided."})

    data_new_user = pd.read_csv(f"../public/users/{username}.csv")
    titles, id_ratings, lst_id_url = cf.recommend(data_new_user, 10)

    jsonifiable_data = [{'anime_id': int(anime_id), 'anime_image_url': anime_image_url} for anime_id, anime_image_url in lst_id_url]
    json_data = json.dumps(jsonifiable_data)

    return jsonify({"results": json_data})


def scroll_to_bottom():
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(1)  # Add a short delay to let the content load

@app.route('/scrap_user', methods=['POST'])
def scrap_user():
    data = request.json
    username = data.get('username')

    url = f"https://myanimelist.net/animelist/{username}"

    driver.get(url)
    max_scroll_attempts = 5
    for _ in range(max_scroll_attempts):
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
    print("\n\n\n\n",id,"\n\n\n\n\n")

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
    fields = ['Name', 'Type', 'Episodes', 'Premiered', 'Studios', 'Rating']
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
                time.sleep(SLEEP_TIME)

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

        box.send_keys(search_query+" screencap imagesize:1920x1080 filetype:jpg")
        box.send_keys(Keys.ENTER)
        time.sleep(SLEEP_TIME)

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
                    15
                ).until(
                    EC.element_to_be_clickable(
                        img_result
                    )
                )
            img_result.click()
                # Hasta aca entro, busco y dio click en la primera imagen
                #print("zzzz")
            time.sleep(SLEEP_TIME)
            time.sleep(SLEEP_TIME)
                #time.sleep(100000)

            actual_imgs = driver.find_element(
                by=By.XPATH,
                value='//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
            )
                
            xpath = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
            wait = WebDriverWait(driver, 10)

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

if __name__ == '__main__':
    app.run(debug=True)