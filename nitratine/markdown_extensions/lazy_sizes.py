import base64
from dataclasses import dataclass
import io
import math
from pathlib import Path
from typing import Tuple

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from PIL import Image

from ..config import POST_SOURCE


@dataclass
class ResizedImage:
    image_bytes: bytes
    original_size: Tuple[int, int]
    resized_size: Tuple[int, int]


class LazySizesImageProcessor(Treeprocessor):
    def run(self, root):
        for element in root.iter('img'):
            src = element.get('src')
            if src.startswith('/posts/'):
                # Identify file
                file = POST_SOURCE / src[len('/posts/'):]
                image = Image.open(str(file))
                # Get the resized image and convert it to b64
                resized_image = self.get_resized_image(file, 15)
                image_bs4 = base64.b64encode(resized_image.image_bytes)
                # Setup img tag
                element.set('class', 'lazyload blur-up')
                element.set('data-src', element.get('src'))
                element.set('src', f"data:image/png;base64, {image_bs4.decode()}")
                element.set('style', f"width: {image.size[0]}px;")

    @staticmethod
    def get_resized_image(path: Path, new_width: int) -> ResizedImage:
        """ Get the bytes for a resized image """
        # Get image and calculate required ratio
        image = Image.open(str(path))
        original_size = image.size
        ratio = new_width / original_size[0]

        # Calculate new size and resize the image
        new_size = (math.floor(original_size[0] * ratio), math.floor(original_size[1] * ratio))
        image.thumbnail(new_size, Image.ANTIALIAS)

        # Turn the image into a bytes object
        bytes_io = io.BytesIO()
        image.save(bytes_io, format='PNG')

        return ResizedImage(bytes_io.getvalue(), original_size, new_size)


class LazySizesImageExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(LazySizesImageProcessor(md), 'inlineimageprocessor', 15)
