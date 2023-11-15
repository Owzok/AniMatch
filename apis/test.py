import requests
import numpy as np

api_url = 'http://localhost:5000/get_info'  # Replace with the actual URL of your API

request_data = {
    'id': 200
}

response = requests.post(api_url, json=request_data)

if response.status_code == 200:
    print("API request was successful.")
    print("Response:", response.json())
else:
    print("API request failed with status code:", response.status_code)
    print("Response:", response.text)