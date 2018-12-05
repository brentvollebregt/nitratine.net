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
        'youtube_data_api_key': ''
    },
    'people': {
        'Brent Vollebregt': 'https://github.com/brentvollebregt'
    },
    'redirects': {
        'home': '',
    },
    'home-tiles': [
        {
            'type': 'raw',
            'link': '/',
            'content': 'Add tiles in config.json'
        }
    ],

}

LOCATION = 'config.json'


def get(*args):
    """ Traverse the config data to get a value """
    traversal = config_data
    try:
        for arg in args:
            traversal = traversal[arg]
    except:
        raise KeyError('Cannot get {0} from {1}'.format(':'.join([str(arg) for arg in args]), LOCATION))
    return traversal


if os.path.exists(LOCATION):
    with open(LOCATION, 'r') as f:
        config_data = json.load(f)
else:
    with open(LOCATION, 'w') as f:
        json.dump(DEFAULT, f, indent=4)
    print('{0} does not exist, a template has been generated'.format(LOCATION))
    raise FileNotFoundError('{0} does not exist'.format(LOCATION))
