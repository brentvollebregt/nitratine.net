import json
import os


DEFAULT = {
    'serve-and-build': {
        'flatpages': {
            'debug': True,
            'extension': '.md',
            'root': 'posts',
            'markdown-extensions': ['codehilite', 'extra', 'toc'],
        },
        'pagination': {
            'max-per-page': 10,
            'pages-either-side-in-nav': 2,
        },
        'paths': {
            'build-destination': 'docs',
            'assets': 'assets',
            'post-assets': 'post-assets',
        }
    },
    'site': {
        'title': 'Nitratine',
        'url': 'https://nitratine.net',
        'domain': 'nitratine.net',
        'about': '',
        'theme_colour': '#343a40',
        'email': 'brent@nitratine.net',
        'youtube_link': 'https://www.youtube.com/PyTutorials',
        'github_username': 'brentvollebregt',
        'default_author': 'Brent Vollebregt',
        'disqus_shortname': 'nitratine',
        'google_analytics_id': '',
        'google_ad_client': '',
        'youtube_channel_name': '',
        'youtube_channel_id': '',
        'youtube_data_api_key': '',
        'category-extra': {
            "YouTube": "&#x1F3A5;",
            "Projects": "&#x1F4BE;",
            "Tutorials": "&#x1F4D6;",
            "Apps": "&#x1F4F1;",
            "Investigations": "&#x1F50D;",
            "General": "&#x1F4F0;"
        }
    },
    'redirects': {
        'home': '',
        'from/this/route': 'to/here',
    },
    'home-tiles': [
        {
            'type': 'image',
            'link': 'https://youtu.be/ksW59gYEl6Q',
            'image_url': 'https://img.youtube.com/vi/ksW59gYEl6Q/mqdefault.jpg'
        },
        {
            'type': 'post',
            'post': 'auto-py-to-exe',
            'reason': 'popular'
        },
        {
            'type': 'img-content',
            'link': 'https://github.com/brentvollebregt/auto-py-to-exe',
            'image_url': '/post-assets/auto-py-to-exe/feature.png',
            'content_raw': '<div class="text-center">Here you can add an image and your own content below</div>'
        },
        {
            'type': 'raw',
            'link': '#',
            'content': 'This is a raw home tiles. Any HTML will be added straight into the template'
        }
    ],

}

LOCATION = 'config.json'
SAMPLE_ADDITION = '.sample'


def get(*args):
    """ Traverse the config data to get a value """
    traversal = config_data
    try:
        for arg in args:
            traversal = traversal[arg]
    except KeyError:
        raise KeyError('Cannot get {0} from {1}'.format(':'.join([str(arg) for arg in args]), LOCATION))
    return traversal


if os.path.exists(LOCATION):
    with open(LOCATION, 'r') as f:
        config_data = json.load(f)
else:
    with open(LOCATION + SAMPLE_ADDITION, 'w') as f:
        json.dump(DEFAULT, f, indent=4)
    print('{0} does not exist, a template has been generated'.format(LOCATION + SAMPLE_ADDITION))
    raise FileNotFoundError('{0} does not exist'.format(LOCATION + SAMPLE_ADDITION))
