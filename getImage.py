from models.engine import storage
from models.story import Story

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os

def getStoryImage(storage, Story, download_path="images"):
    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # Retry strategy
    retry_strategy = Retry(
        total=5,  # number of retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # Changed to allowed_methods
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    stories = storage.all(Story)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    download_path = os.path.join(os.path.dirname(__file__), 'uploads')
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print(stories)
    for story in stories.values():
        image_url = story.image
        if image_url and image_url.startswith('https://'):
            try:
                response = http.get(image_url, headers=headers, verify=False)
                print(response.status_code, response.url)
                
                if response.status_code == 200:
                    # Define the path to save the image
                    image_filename = os.path.join(download_path, f"{story.id}.jpg")
                    
                    # Save the image content to a file
                    with open(image_filename, 'wb') as f:
                        f.write(response.content)
                    
                    # Update the story object with the local image path
                    story.image = f"{story.id}.jpg"
                    story.save()
                    storage.save()
                    print(f"Image saved to {story.image}")
                else:
                    print(f"Failed to fetch image from {image_url}: Status code {response.status_code}")
            except requests.RequestException as e:
                print(f"Failed to fetch image from {image_url}: {e}")

# Example usage (assuming `storage` and `Story` are defined):
getStoryImage(storage, Story)