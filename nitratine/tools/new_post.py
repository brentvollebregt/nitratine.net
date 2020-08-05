import os
import string
import time
from urllib.parse import quote_plus

from ..config import POST_SOURCE, POST_FILENAME, POST_EXTENSION
from ..site import posts


def new_post():
    """ Automatically setup a new posts file structure """
    title = input('Title: ')
    post_id = quote_plus(''.join(
        [i for i in title.lower().replace(' ', '-') if i in f'{string.ascii_letters}{string.digits}-']
    ))
    post_directory = os.path.join(POST_SOURCE, post_id)
    print('Post will be found in {0}'.format(post_directory))

    # Category selection
    while True:
        print('Select a category from the following list by its index')
        categories = list(posts.posts_by_category())
        for i, value in enumerate(categories):
            print('{0}) {1}'.format(i, value))
        selection = input('Category: ')
        try:
            category = categories[int(selection)]
            break
        except ValueError:
            print('Please provide an option number')
        except IndexError:
            print('That index does not exist')

    tags = input('Tags (separated by a space): ').lower().split(' ')

    # Create the directory
    if not os.path.isdir(post_directory):
        os.makedirs(post_directory)

    # Write post file
    file_path = os.path.join(post_directory, f'{POST_FILENAME}{POST_EXTENSION}')
    f = open(file_path, 'w')
    f.write('title: "{0}"\n'.format(title))
    f.write('date: {0}\n'.format(time.strftime('%Y-%m-%d')))
    f.write('category: {0}\n'.format(category))
    f.write('tags: [{0}]\n'.format(', '.join(tags)))
    f.write('feature: feature.png\n')
    f.write('description: ""\n')
    f.write('\n[TOC]\n')
    f.write('\n## Content\n')
    f.close()
    print('\nCreated {0}'.format(file_path))

    # Create feature image file (no contents)
    feature_img = os.path.join(post_directory, 'feature.png')
    if not os.path.isfile(feature_img):
        f = open(feature_img, 'w')
        f.close()
        print('Created: {0}'.format(feature_img))
