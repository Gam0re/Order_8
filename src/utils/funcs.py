import requests
from PIL import Image
from io import BytesIO


async def get_image_size(url):
    try:
        response = requests.head(url)
        headers = response.headers
        content_length = headers.get('Content-Length')
        if content_length:
            size_in_bytes = int(content_length)
            size_in_mb = size_in_bytes / 1000000
            return size_in_mb
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None


async def get_image_ratio(url):
    try:
        response = requests.get(url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        width, height = image.size
        aspect_ratio = width / height
        return width, height, aspect_ratio
    except Exception as e:
        print("Error:", e)
        return None, None, None
