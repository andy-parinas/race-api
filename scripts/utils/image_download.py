import os
import requests
from requests.exceptions import RequestException


def image_download(image_url):
    try:
        response = requests.get(image_url)
        image_data = response.content

        filename = os.path.basename(image_url)

        return image_data, filename
    except RequestException:
        print("Error Downloading the Image")
        return None
