import base64
from dataclasses import dataclass
from functools import wraps
import io
from pathlib import Path
from typing import Tuple

from bs4 import BeautifulSoup
from PIL import Image

from ..config import POST_SOURCE


def apply_lazy_load_to_supported_images(f):
    """
    Decorator to apply lazyload to images that are supported.
    lazyload images are delayed image loading and blur-up
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = f(*args, **kwargs)
        soup = BeautifulSoup(result, 'html.parser')

        # Replace all images in main content with lazyload images
        main_element = soup.find('main')
        if main_element is not None:
            for img in main_element.find_all('img'):
                if img.attrs['src'].startswith('/posts/'):
                    # Identify file and get width
                    file = POST_SOURCE / img.attrs['src'][len('/posts/'):]
                    image = Image.open(str(file))
                    image_width = image.size[0]
                    image_height = image.size[1]
                    image.close()

                    # Get the resized image and convert it to b64
                    resized_image = __get_resized_image(file, 15)
                    image_bs4 = base64.b64encode(resized_image.image_bytes)

                    # Setup img tag
                    img.attrs['class'] = 'lazyload blur-up'
                    img.attrs['data-src'] = img.attrs['src']
                    img.attrs['src'] = f"data:image/png;base64, {image_bs4.decode()}"
                    img.attrs['width'] = str(image_width)
                    img.attrs['height'] = str(image_height)
                    img.attrs['style'] = f'{img.attrs.get("style", "")}; aspect-ratio: {image_width}/{image_height}; height: auto;'

        return str(soup)
    return decorated_function


@dataclass
class __ResizedImage:
    image_bytes: bytes
    original_size: Tuple[int, int]
    resized_size: Tuple[int, int]


def __get_resized_image(path: Path, new_width: int) -> __ResizedImage:
    """ Get the bytes for a resized image """
    # Get image and calculate required ratio
    image = Image.open(str(path))
    original_size = image.size
    ratio = new_width / original_size[0]

    # Calculate new size and resize the image
    new_size = (round(original_size[0] * ratio), round(original_size[1] * ratio))
    image.thumbnail(new_size, Image.LANCZOS)

    # Turn the image into a bytes object
    bytes_io = io.BytesIO()
    image.save(bytes_io, format='PNG')
    image.close()

    return __ResizedImage(bytes_io.getvalue(), original_size, new_size)
