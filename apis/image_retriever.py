import requests
from bs4 import BeautifulSoup

def google_image_search(query, size="1920x1080"):
    search_url = f"https://www.google.com/search?q={query}+imagesize:{size}&tbm=isch"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            img_element = soup.find("img")
            if img_element:
                image_url = img_element.get("src")
                return image_url

        return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    query = "nature landscape"  # Replace with your search query
    image_url = google_image_search(query)

    if image_url:
        print("First image URL:", image_url)
    else:
        print("No images found.")