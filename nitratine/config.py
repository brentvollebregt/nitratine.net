import os
from pathlib import Path

from dotenv import load_dotenv


__module_directory_path = Path(__file__).resolve().parent

load_dotenv(dotenv_path=(__module_directory_path / '../.env').resolve(), verbose=True)

FREEZE_DESTINATION = (__module_directory_path / '../build').resolve()  # Output location for the build/freeze
POST_SOURCE = (__module_directory_path / '../posts').resolve()  # Source directory for posts
POST_FILENAME = 'post'  # Name of files in post folder to be used as post source (no extension)
POST_EXTENSION = '.md'  # The extension for the POST_FILENAME files

PAGINATION_PAGE_MAX = 10  # Max amount of posts per page
PAGINATION_EITHER_SIDE = 2  # Number of tiles beside current page in pagination navigation e.g. 2 = P P C N N


class SiteConfig:
    def __init__(self, data: dict):
        self.title = data['title']
        self.url = data['url']
        self.domain = data['domain']
        self.about = data['about']
        self.theme_colour = data['theme_colour']
        self.email = data['email']
        self.youtube_link = data['youtube_link']
        self.github_username = data['github_username']
        self.default_author = data['default_author']
        self.disqus_shortname = data['disqus_shortname']
        self.google_analytics_id = data['google_analytics_id']
        self.google_adsense_publisher_id = data['google_adsense_publisher_id']
        self.youtube_channel_name = data['youtube_channel_name']
        self.youtube_channel_id = data['youtube_channel_id']
        self.youtube_data_api_key = data['youtube_data_api_key']
        self.category_icons = data['category-extra']
        self.featured_sites = data['featured-sites']

        # Validate featured sites
        for site in self.featured_sites:
            assert 'title' in site
            assert 'url' in site and site['url'] != ''
            assert 'image_url' in site and site['image_url'] != ''


class Config:
    def __init__(self, data: dict):
        self.site = SiteConfig(data['site'])
        self.redirects = data['redirects']
        self.home_tiles = data['home-tiles']

        # Validate home tiles
        for tile in self.home_tiles:
            assert 'type' in tile  # All must have a type
            if tile['type'] == 'post-image':
                assert 'post' in tile
                assert 'image_url' in tile
            elif tile['type'] == 'post':
                assert 'post' in tile
                assert 'reason' in tile
            elif tile['type'] == 'raw':
                assert 'link' in tile
                assert 'content' in tile
            else:
                raise Exception(f"Unexpected home tile type: {tile['type']}")


config_data = {
    'site': {
        'title': 'Nitratine',
        'url': 'https://nitratine.net',
        'domain': 'nitratine.net',
        'about': 'Owner of <a href=\"https://www.youtube.com/PyTutorials\">PyTutorials</a> and creator of <a href=\"https://github.com/brentvollebregt/auto-py-to-exe\">auto-py-to-exe</a>. I enjoy making quick tutorials for people new to particular topics in Python and  tools that help fix small things.',
        'theme_colour': '#343a40',
        'email': 'brent@nitratine.net',
        'youtube_link': 'https://www.youtube.com/PyTutorials',
        'github_username': 'brentvollebregt',
        'default_author': 'Brent Vollebregt',
        'disqus_shortname': 'nitratine',
        'google_analytics_id': 'UA-117153268-2',
        'google_adsense_publisher_id': 'pub-6407227183932047',
        'youtube_channel_name': 'PrivateSplat',
        'youtube_channel_id': 'UCesEknt3SRX9R9W_f93Tb7g',
        'youtube_data_api_key': os.getenv('YOUTUBE_DATA_API_KEY'),
        'category-extra': {
            'YouTube': '&#x1F3A5;',
            'Projects': '&#x1F4BE;',
            'Tutorials': '&#x1F4D6;',
            'Apps': '&#x1F4F1;',
            'Investigations': '&#x1F50D;',
            'Tools': '&#x1F6E0;',
            'Snippets': '&#x2702;',
            'General': '&#x1F4F0;'
        },
        'featured-sites': [
            {
                'title': 'Emotionify',
                'url': 'https://emotionify.nitratine.net/',
                'image_url': '/static/img/featured-sites/emotionify.png',
            },
            {
                'title': 'Spotify Lyrics Viewer',
                'url': 'https://spotify-lyrics-viewer.nitratine.net/',
                'image_url': '/static/img/featured-sites/spotify-lyrics-viewer.png',
            },
            {
                'title': 'Hit Counter',
                'url': 'https://hitcounter.pythonanywhere.com/',
                'image_url': '/static/img/featured-sites/hit-counter.png',
            },
            {
                'title': 'Monopoly Money',
                'url': 'https://monopoly-money.nitratine.net/',
                'image_url': '/posts/monopoly-money/banner.png',
            }
        ]
    },
    'redirects': {
        'tag': 'blog/tags',
        'category': 'blog/categories',
        'archive': 'blog/archive',
        'donations': 'about',
        'blog/post': 'blog',
        'colour': 'blog/post/colour',
        'finding-emotion-in-music-with-python': 'blog/post/finding-emotion-in-music-with-python',
        'interesting-sites': 'blog/post/interesting-sites',
        'randomly-generating-numbers-to-fulfil-an-integer-range': 'blog/post/randomly-generating-numbers-to-fulfil-an-integer-range',
        'convert-py-to-exe': 'blog/post/convert-py-to-exe',
        'get-wifi-passwords-with-python': 'blog/post/get-wifi-passwords-with-python',
        'how-to-setup-pythons-pip': 'blog/post/how-to-setup-pythons-pip',
        'how-to-get-mouse-clicks-with-python': 'blog/post/how-to-get-mouse-clicks-with-python',
        'python-keylogger': 'blog/post/python-keylogger',
        'simulate-keypresses-in-python': 'blog/post/simulate-keypresses-in-python',
        'quick-script': 'blog/post/quick-script',
        'lucy-in-the-sky-with-emotion': 'blog/post/lucy-in-the-sky-with-emotion',
        'monopoly-money': 'blog/post/monopoly-money',
        'mp3-itunes-downloader': 'blog/post/mp3-itunes-downloader',
        'spotify-playlist-downloader': 'blog/post/spotify-playlist-downloader',
        'adding-snow-to-your-website': 'blog/post/adding-snow-to-your-website',
        'change-file-modification-time-in-python': 'blog/post/change-file-modification-time-in-python',
        'the-nitratine-project': 'blog/post/the-nitratine-project',
        'how-to-make-hotkeys-in-python': 'blog/post/how-to-make-hotkeys-in-python',
        'simulate-mouse-events-in-python': 'blog/post/simulate-mouse-events-in-python',
        'how-to-send-an-email-with-python': 'blog/post/how-to-send-an-email-with-python',
        'python-retweet-bot': 'blog/post/python-retweet-bot',
        'python-auto-clicker': 'blog/post/python-auto-clicker',
        'auto-py-to-exe': 'blog/post/auto-py-to-exe',
        'hit-counter': 'blog/post/hit-counter',
        'github-badges': 'blog/post/github-badges',
        'my-desktop-backgrounds': 'blog/post/my-desktop-backgrounds',
        'how-to-add-a-custom-domain-to-a-github-pages-site': 'blog/post/how-to-add-a-custom-domain-to-a-github-pages-site',
        'python-threading-basics': 'blog/post/python-threading-basics',
        'python-gui-using-chrome': 'blog/post/python-gui-using-chrome',
        'python-sqlite3-basics': 'blog/post/python-sqlite3-basics',
        'price-per-unit': 'blog/post/price-per-unit',
        'putting-auto-py-to-exe-on-pypi': 'blog/post/putting-auto-py-to-exe-on-pypi',
        'media-picker': 'blog/post/media-picker',
        'python-guis-with-pyqt': 'blog/post/python-guis-with-pyqt',
        'how-to-clean-a-twitter-account-with-jquery': 'blog/post/how-to-clean-a-twitter-account-with-jquery',
        'multi-clipboard': 'blog/post/multi-clipboard',
        'uow-moodle-rwa-ignorer': 'blog/post/uow-moodle-rwa-ignorer',
        'am-i-a-participant': 'blog/post/am-i-a-participant',
        'asymmetric-encryption-and-decryption-in-python': 'blog/post/asymmetric-encryption-and-decryption-in-python',
        'common-issues-when-using-auto-py-to-exe': 'blog/post/issues-when-using-auto-py-to-exe',
        'encryption-and-decryption-in-python': 'blog/post/encryption-and-decryption-in-python',
        'blog/post/common-issues-when-using-auto-py-to-exe': 'blog/post/issues-when-using-auto-py-to-exe',
        'blog/post/who-is-on-my-network': 'blog/post/whos-on-my-network'
    },
    'home-tiles': [
        {
            'type': 'raw',
            'link': '/blog/post/auto-py-to-exe/',
            'content': """
                <img class="card-img-top" src="/posts/auto-py-to-exe/feature.png" alt="Thumbnail">
                <div class="card-body">
                    <div class=\"text-center\">
                        <h5 class=\"card-title mb-1\">Auto Py to Exe</h5>
                        <img alt=\"Total downloads for auto-py-to-exe project\" src=\"https://pepy.tech/badge/auto-py-to-exe\">
                        <br>
                        <small class=\"text-muted\">pip install auto-py-to-exe</small>
                    </div>
                </div>
            """
        },
        {
            'type': 'post-image',
            'post': 'encryption-and-decryption-in-python',
            'image_url': 'https://img.youtube.com/vi/H8t4DJ3Tdrg/mqdefault.jpg'
        },
        {
            'type': 'post',
            'post': 'issues-when-using-auto-py-to-exe',
            'reason': 'Popular'
        },
        {
            'type': 'raw',
            'link': '/blog/post/emotionify/',
            'content': """
                <div class=\"text-center\">
                    <img class=\"card-img-top\" src=\"/posts/emotionify/emotionify-banner.png\" alt=\"Emotionify Banner\" style=\"padding: 20px 10px 20px 10px\">
                    <p class=\"mx-2\">Sort Spotify playlists using Spotify's pre-calculated audio features to attempt to emotionally gradient playlists.</p>
                </div>
            """
        },
        {
            'type': 'post',
            'post': 'python-encryption-and-decryption-with-pycryptodome',
            'reason': 'New'
        },
        {
            'type': 'post-image',
            'post': 'python-guis-with-pyqt',
            'image_url': 'https://img.youtube.com/vi/ksW59gYEl6Q/mqdefault.jpg'
        },
        {
            'type': 'post-image',
            'post': 'how-to-send-an-email-with-python',
            'image_url': 'https://img.youtube.com/vi/YPiHBtddefI/mqdefault.jpg'
        },
        {
            'type': 'post',
            'post': 'python-requests-tutorial',
            'reason': 'New'
        },
        {
            'type': 'post',
            'post': 'encryption-and-decryption-in-python',
            'reason': 'Popular'
        },
        {
            'type': 'post-image',
            'post': 'auto-py-to-exe',
            'image_url': 'https://img.youtube.com/vi/OZSZHmWSOeM/mqdefault.jpg'
        },
        {
            'type': 'raw',
            'link': '/blog/post/spotify-lyrics-viewer/',
            'content': """
                <div class=\"text-center\">
                    <img class=\"card-img-top\" src=\"/posts/spotify-lyrics-viewer/spotify-lyrics-viewer-banner.png\" alt=\"Spotify Lyrics Viewer\" style=\"padding: 20px 10px 20px 10px\">
                    <p class=\"mx-2\">Spotify Lyrics Viewer is a tool that allows you to view the lyrics of the current playing song on Spotify by simply signing in.</p>
                </div>
            """
        },
        {
            'type': 'post',
            'post': 'how-to-hash-passwords-in-python',
            'reason': 'New'
        },
        {
            'type': 'post',
            'post': 'simulate-keypresses-in-python',
            'reason': 'Popular'
        }
    ]
}

config = Config(config_data)
