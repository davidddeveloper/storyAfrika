from models.engine import storage
from models.user import User

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import uuid

def getUserAvatar(storage, User, download_path="images"):
    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # Retry strategy
    retry_strategy = Retry(
        total=5,  # number of retries
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]  # Changed to allowed_methods
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    users = storage.all(User)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    download_path = os.path.join(os.path.dirname(__file__), 'uploads')
    if not os.path.exists(download_path):
        os.makedirs(download_path)


    for user in users.values():
        image_url = user.avatar
        if True:
            try:
                response = http.get('https://picsum.photos/600', headers=headers, verify=False)
                print(response.status_code, response.url)

                if response.status_code == 200:
                    # Define the path to save the image
                    filename = uuid.uuid4()
                    image_filename = os.path.join(download_path, f"{filename}.jpg")

                    # Save the image content to a file
                    with open(image_filename, 'wb') as f:
                        f.write(response.content)

                    # Update the story object with the local image path
                    user.avatar = f"{filename}.jpg"
                    user.save()
                    storage.save()
                    print(f"Image saved to {user.avatar}")
                else:
                    print(f"Failed to fetch image from {image_url}: Status code {response.status_code}")
            except requests.RequestException as e:
                print(f"Failed to fetch image from {image_url}: {e}")

# Example usage (assuming `storage` and `Story` are defined):
getUserAvatar(storage, User)