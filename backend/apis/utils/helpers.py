import os
import concurrent.futures
from bs4 import BeautifulSoup
import requests

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

from PIL import Image                       # save image from google
import base64                               # save image in base 64
from io import BytesIO                      # save image

from typing import List, Dict, Tuple, Optional

from difflib import SequenceMatcher         # search title by name
import time

#TODO: do ospath join and dirname to get the path dynamically
#TODO: wtf is ranked spot in Home?
#TODO: colab is dead, content fails and the rest i didnt try. network is the only thing alive
#TODO: Delete the asdasdsad directory. Como usar interactive? ni lo veo weon

MAIN_PATH = "../../frontend/public/download/profiles/"
RETURNABLE_PATH = "/download/profiles/"


# Retrieval

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def retrieve_id(title, df):
    if title is None:
        return None
    df['r'] = df.apply(lambda x: similar(x.Name, title), axis=1)
    return df['r'].idxmax()

def do_filtering(data, min_score=1, max_score=10, min_episodes=1, 
                 max_episodes=10000, min_year=1970, max_year=2023, 
                 prequels=False, mature=False):
    if max_episodes == 100: 
        max_episodes = 10000
    return data[(data['Score'] >= min_score) & (data['Score'] <= max_score) & 
                (data['Episodes'] >= min_episodes) & (data['Episodes'] <= max_episodes) & 
                (data['Year'] >= min_year) & (data['Year'] <= max_year) & 
                ((data['Prequel'] == int(prequels)) | (data['Prequel'] == 0)) & 
                ((data['Hentai'] == int(mature)) | (data['Hentai'] == 0))]

def get_length_text(id, synopsis):
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

def startup_driver():
    driver = None
    try: 
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            #service=service,
            options=chrome_options
        )
    except Exception as e:
        print("Error with webscraping & ChromeDriver:",e)
    
    return driver

def scroll_to_bottom(driver):
    '''Scroll to the bottom of the page'''
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        WebDriverWait(driver, 7)

        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            element = driver.find_element(
                by=By.CSS_SELECTOR,
                value='.YstHxe input'
            )
            element.click()
            WebDriverWait(driver, 1)
        except:
            pass

        if new_height == last_height:
            break

        last_height = new_height
"""
def download_google_images(search_query: str, mal_id: int, driver, save_path) -> None:
    def save_image(image_url):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image.save(f"{save_path}/{mal_id}.jpg")
                print(f"Image saved as {mal_id}.jpg")
                return 200
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                return response.status_code
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None

    def save_base64(b64):
        try:
            base64_data = b64.split(',')[1]
            image_data = base64.b64decode(base64_data)
            image_stream = BytesIO(image_data)
            image = Image.open(image_stream)
            image.save(f'{save_path}/{mal_id}.jpg', 'JPEG')
            print(f"Image saved as {mal_id}.jpg")
            image_stream.close()
        except Exception as e:
            print(f"Error processing base64 image: {e}")

    url = 'https://www.google.com/imghp'  # Correct URL for Google Images

    driver.get(url)

    # Wait for the search input to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))

    # Search for the query
    search_box = driver.find_element(By.NAME, 'q')
    print("Searching for", search_query)
    search_box.send_keys(search_query + " anime imagesize:1920x1080 filetype:jpg OR filetype:png")
    search_box.send_keys(Keys.ENTER)

    # Wait for images to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.rg_i.Q4LuWd")))

    img_results = driver.find_elements(By.CSS_SELECTOR, "img.rg_i.Q4LuWd")
    print(f'Total images found: {len(img_results)}')

    for img_result in img_results:
        try:
            # Wait for the image to be clickable
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(img_result))
            img_result.click()

            # Wait for the larger image to load
            xpath = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]'
            large_img = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Extract image URL or base64 data
            img_url = large_img.get_attribute("src")
            if img_url.startswith('https'):
                print("Downloading image from URL")
                if save_image(img_url) == 200:
                    return
            elif img_url.startswith('data:image/'):
                print("Processing base64 image data")
                save_base64(img_url)
                return
        except Exception as e:
            print(f"Error during image processing: {e}")
            continue
"""
def download_google_images(search_query: str, mal_id: int, driver, save_path) -> None:
    def save_image(image_url):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image.save(f"{save_path}{mal_id}.jpg")
                print(f"Image saved as {mal_id}.jpg")
                return 200
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                return response.status_code
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None

    def save_base64(b64):
        try:
            base64_data = b64.split(',')[1]
            image_data = base64.b64decode(base64_data)
            image_stream = BytesIO(image_data)
            image = Image.open(image_stream)
            image.save(f'{save_path}/{mal_id}.jpg', 'JPEG')
            print(f"Image saved as {mal_id}.jpg")
            image_stream.close()
        except Exception as e:
            print(f"Error processing base64 image: {e}")

    url = 'https://www.google.com/imghp'  # Correct URL for Google Images

    driver.get(url)

    # Wait for the search input to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))

    # Search for the query
    search_box = driver.find_element(By.NAME, 'q')
    print("Searching for", search_query)
    search_box.send_keys(search_query + " anime imagesize:1920x1080 filetype:jpg OR filetype:png")
    search_box.send_keys(Keys.ENTER)

    # Wait for images to load
    elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//*[@jsname='dTDiAc']")))

    img_results = driver.find_elements(By.XPATH, "//*[@jsname='dTDiAc']")
    print(f'Total images found: {len(img_results)}')

    for img_result in img_results:
        try:
            # Wait for the image to be clickable
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(img_result))
            img_result.click()

            # Wait for the larger image to load
            xpath = "//*[@jsname='kn3ccd']"
            large_img = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Extract image URL or base64 data
            img_url = driver.find_element(By.XPATH, "//*[@jsname='kn3ccd']").get_attribute('src')
            print("Downloading image from URL")
            if save_image(img_url) == 200:
                return
        except Exception as e:
            print(f"Error during image processing: {e}")
            continue

def save_image(anime_id: int) -> Tuple[int, Optional[str]]:
    full_url = MAIN_PATH+f"{anime_id}.jpg"
    returnable_url = RETURNABLE_PATH+f"{anime_id}.jpg"

    if os.path.isfile(full_url):
        return (anime_id, returnable_url)
    else:
        print("No hay imagen de ", anime_id)
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
        
def get_lst_images(lst_recommend: List[int]) -> Dict[int, str]:
    """
    Concurrently saves images for a list of recommended anime
    """
    imgs_anime = {}
    with concurrent.futures.ThreadPoolExecutor() as mainExecutor:
        future_execution = [mainExecutor.submit(save_image, anime)
                            for anime in lst_recommend]
        for future in concurrent.futures.as_completed(future_execution):
            result = future.result()
            if result is not None:
                anime_id, image_path = result
                imgs_anime[anime_id] = image_path
    return imgs_anime