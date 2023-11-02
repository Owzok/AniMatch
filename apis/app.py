from flask import Flask, request, jsonify
from content import ContentBasedRecommender
from flask_cors import CORS
import time
import base64
from io import BytesIO
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
import requests
from PIL import Image

app = Flask(__name__)
CORS(app) 
cb = ContentBasedRecommender()

cwd = os.getcwd()
IMAGE_FOLDER = '../public/download/'
os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)

chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service,
    options=chrome_options
)

SLEEP_TIME = 1

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.json
    title = data.get('title')
    k = data.get('k')

    if not title or k is None:
        return jsonify({"error": "Invalid request. Make sure 'title' and 'k' are provided."}), 400

    recommendations = cb.recommend(title, k)
    return jsonify({"recommendations": recommendations})


@app.route('/scrape_image', methods=['POST'])
def scrape_image():
    data = request.json
    search_query = data.get('search_query')
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
                image.save(f"../public/download/{mal_id}.jpg")

                print(f"Image saved as {mal_id}.jpg")
            else:
                print(f"Failed to download image. Status code: {response.status_code}")

        def save_base64(b64, title):
            try:
                base64_data = b64.split(',')[1]
                image_data = base64.b64decode(base64_data)
                image_stream = BytesIO(image_data)
                image = Image.open(image_stream)
                image.save(f'../public/download/{search_query}.jpg', 'JPEG')
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

        box.send_keys(search_query+" imagesize:1920x1080")
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
                save_image(img_url)
                return

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