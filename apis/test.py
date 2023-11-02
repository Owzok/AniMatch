import requests

# Define the API endpoint URL
api_url = 'http://localhost:5000/scrape_image'  # Replace with the actual URL of your API

# Define the request data (search_query and num_images)
request_data = {
    'search_query': 'Mawaru Penguindrum',
    'id': '10721',  # Change the number of images as needed
}

# Send a POST request to the API
response = requests.post(api_url, json=request_data)

# Check the response
if response.status_code == 200:
    print("API request was successful.")
    print("Response:", response.json())
else:
    print("API request failed with status code:", response.status_code)
    print("Response:", response.text)