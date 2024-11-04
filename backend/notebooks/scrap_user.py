from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

url = "https://myanimelist.net/animelist/Owzok"

chrome_options = ChromeOptions()

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service,
    options=chrome_options
)

driver.get(url)

def scroll_to_bottom():
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(1)  # Add a short delay to let the content load

max_scroll_attempts = 5

for _ in range(max_scroll_attempts):
    before_scroll = driver.execute_script("return document.body.scrollHeight;")
    scroll_to_bottom()
    after_scroll = driver.execute_script("return document.body.scrollHeight;")

time.sleep(5)

list_items = driver.find_elements(By.CLASS_NAME, "list-item")

anime_list = []

for item in list_items:
    m_anime = {}

    link = item.find_element(By.CLASS_NAME, "link")
    href = link.get_attribute("href")
    
    score_label = item.find_element(By.CLASS_NAME, "score-label").text
    text = link.text
    
    m_anime['user_id'] = 786
    m_anime['anime_id'] = href.split("/")[4]
    m_anime['rating'] = score_label
    if score_label != "-":
        anime_list.append(m_anime)

    #print(f"Href: {href}, Score-Label: {score_label}, Text: {text}")

driver.quit()

df = pd.DataFrame(anime_list)
df.to_csv("scrapped.csv", index=False)