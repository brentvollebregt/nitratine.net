import os
from pathlib import Path

from flask_frozen import Freezer

from .config import FREEZE_DESTINATION, POST_SOURCE, POST_FILENAME, POST_EXTENSION, ASSETS_LOCATION
from .site import app, posts


app.config['FREEZER_DESTINATION'] = FREEZE_DESTINATION
freezer = Freezer(app)


@freezer.register_generator
def blog_post():
    """ Freezer function to identify all posts """
    all_posts = posts.get_posts(hidden=True)
    for post in all_posts:
        print(f'Post: {post.path}')
        yield {'path': post.path}


@freezer.register_generator
def assets():
    """ Freezer function to identify all assets """
    location = ASSETS_LOCATION
    for root, dirs, files in os.walk(location, topdown=False):
        root_path = Path(root)
        for name in files:
            path_in_location = root_path.relative_to(location) / name
            print(f'Asset: {path_in_location}')
            yield {'path': str(path_in_location).replace('\\', '/')}


@freezer.register_generator
def post_assets():
    """ Freezer function to identify all post assets (not the post .md file) """
    location = POST_SOURCE
    for root, dirs, files in os.walk(location, topdown=False):
        root_path = Path(root)
        for name in files:
            if name == f'{POST_FILENAME}{POST_EXTENSION}':
                continue  # No need to freeze this file
            path_in_location = root_path.relative_to(location) / name
            print(f'Post Asset: {path_in_location}')
            yield {'path': str(path_in_location).replace('\\', '/')}
