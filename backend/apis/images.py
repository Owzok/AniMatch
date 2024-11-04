import time
import base64
from io import BytesIO
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from PIL import Image

cwd = os.getcwd()
IMAGE_FOLDER = 'download'
os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service
)

SLEEP_TIME = 1

def download_google_images(search_query: str, number_of_images: int) -> str:
    '''Download google images with this function\n
       Takes -> search_query, number_of_images\n
       Returns -> None
    '''

    def save_image(image_url):
        print(image_url)
        response = requests.get(image_url)

        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            image.save(f"./download/{search_query}.jpg")

            print(f"Image saved as {mal_id}.jpg")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

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
        try:
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
        except:
            print("EXCEPT")
            return


tags = [
    'Demon Slayer Douma'
]

for tag in tags:
    print(f'{"="*10} Downloding for the tag - {tag} {"="*10}')
    download_google_images(
        tag,
        5
    )
    print(f'{"="*10} Finished downloding for the tag - {tag} {"="*10}')

driver.quit()