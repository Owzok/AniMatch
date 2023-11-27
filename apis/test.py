import requests
import numpy as np

api_url = 'http://127.0.0.1:5000/recommend'  # Replace with the actual URL of your API

request_data = {
    'username': 'Owzok'
}

response = requests.post(api_url, json=request_data)

if response.status_code == 200:
    print("API request was successful.")
    print("Response:", response.json())
else:
    print("API request failed with status code:", response.status_code)
    print("Response:", response.text)