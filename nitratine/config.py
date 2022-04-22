from dataclasses import dataclass
import os
from pathlib import Path
from typing import List, Optional, Dict

from dotenv import load_dotenv


__module_directory_path = Path(__file__).resolve().parent

load_dotenv(dotenv_path=(__module_directory_path / '../.env').resolve(), verbose=True)

FREEZE_DESTINATION = (__module_directory_path / '../build').resolve()  # Output location for the build/freeze
POST_SOURCE = (__module_directory_path / '../posts').resolve()  # Source directory for posts
POST_FILENAME = 'post'  # Name of files in post folder to be used as post source (no extension)
POST_EXTENSION = '.md'  # The extension for the POST_FILENAME files

PAGINATION_PAGE_MAX = 10  # Max amount of posts per page
PAGINATION_EITHER_SIDE = 2  # Number of tiles beside current page in pagination navigation e.g. 2 = P P C N N


@dataclass
class CategoryPrefix:
    category: str
    prefix: str


@dataclass
class FeaturedSite:
    title: str
    url: str
    image_url: str


@dataclass
class FeaturedPost:
    type: str
    post: str
    content: Optional[str] = None


class __DefaultSiteConfig:
    def __init__(self):
        self.title = 'Nitratine'
        self.url = 'https://nitratine.net'
        self.domain = 'nitratine.net'
        self.about = 'Owner of <a href="https://www.youtube.com/PyTutorials">PyTutorials</a> and creator of <a href="https://github.com/brentvollebregt/auto-py-to-exe">auto-py-to-exe</a>. I enjoy making quick tutorials for people new to particular topics in Python and tools that help fix small things.'
        self.theme_colour = '#343a40'
        self.email = 'brent@nitratine.net'
        self.youtube_link = 'https://www.youtube.com/PyTutorials'
        self.github_username = 'brentvollebregt'
        self.default_author = 'Brent Vollebregt'
        self.disqus_shortname = 'nitratine'
        self.google_analytics_id = 'G-EB27CZP773'
        self.google_analytics_id_old = 'UA-117153268-2'  # Universal Analytics Id that should be removed around 1 July 2023
        self.google_adsense_publisher_id = 'pub-6407227183932047'
        self.youtube_channel_name = 'PrivateSplat'
        self.youtube_channel_id = 'UCesEknt3SRX9R9W_f93Tb7g'
        self.youtube_data_api_key = os.getenv('YOUTUBE_DATA_API_KEY')
        self.category_prefixes: Dict[str, str] = {
            'YouTube': '&#x1F3A5;',
            'Projects': '&#x1F4BE;',
            'Tutorials': '&#x1F4D6;',
            'Apps': '&#x1F4F1;',
            'Investigations': '&#x1F50D;',
            'Tools': '&#x1F6E0;',
            'Snippets': '&#x2702;',
            'General': '&#x1F4F0;'
        }
        self.featured_sites: List[FeaturedSite] = [
            FeaturedSite(
                title='Emotionify',
                url='https://emotionify.nitratine.net/',
                image_url='/static/img/featured-sites/emotionify.png',
            ),
            FeaturedSite(
                title='Spotify Lyrics Viewer',
                url='https://spotify-lyrics-viewer.nitratine.net/',
                image_url='/static/img/featured-sites/spotify-lyrics-viewer.png',
            ),
            # FeaturedSite(
            #     title='Hit Counter',
            #     url='https://hitcounter.pythonanywhere.com/',
            #     image_url='/static/img/featured-sites/hit-counter.png',
            # ),
            FeaturedSite(
                title='Monopoly Money',
                url='https://monopoly-money.nitratine.net/',
                image_url='/posts/monopoly-money/banner.png',
            )
        ]


site_config = __DefaultSiteConfig()

featured_posts: List[FeaturedPost] = [
    FeaturedPost(
        type='raw',
        post='auto-py-to-exe',
        content="""
            <img class="card-img-top" src="/posts/auto-py-to-exe/feature.png" alt="Thumbnail">
            <div class="card-body">
                <div class=\"text-center\">
                    <h2 class=\"h4 card-title mb-1\">Auto Py to Exe</h2>
                    <img alt=\"Total downloads for auto-py-to-exe project\" src=\"https://pepy.tech/badge/auto-py-to-exe\">
                    <br>
                    <small class=\"text-muted\">pip install auto-py-to-exe</small>
                </div>
            </div>
        """
    ),
    FeaturedPost(type='post-image', post='encryption-and-decryption-in-python',),
    FeaturedPost(type='post', post='issues-when-using-auto-py-to-exe'),
    FeaturedPost(type='post-image', post='how-to-send-an-email-with-python'),
    FeaturedPost(
        type='raw',
        post='emotionify',
        content="""
            <div class=\"text-center\">
                <img class=\"card-img-top\" src=\"/posts/emotionify/emotionify-banner.png\" alt=\"Emotionify Banner\" style=\"padding: 20px 10px 20px 10px\">
                <p class=\"mx-2\">Sort Spotify playlists using Spotify's pre-calculated audio features to attempt to emotionally gradient playlists.</p>
            </div>
        """
    ),
    FeaturedPost(type='post', post='python-encryption-and-decryption-with-pycryptodome'),
    FeaturedPost(type='post', post='python-requests-tutorial'),
    FeaturedPost(type='post', post='python-face-recognition-tutorial'),
    FeaturedPost(type='post', post='simulate-keypresses-in-python'),
    FeaturedPost(type='post-image', post='python-guis-with-pyqt'),
    FeaturedPost(
        type='raw',
        post='spotify-lyrics-viewer',
        content="""
            <div class=\"text-center\">
                <img class=\"card-img-top\" src=\"/posts/spotify-lyrics-viewer/spotify-lyrics-viewer-banner.png\" alt=\"Spotify Lyrics Viewer\" style=\"padding: 20px 10px 20px 10px\">
                <p class=\"mx-2\">Spotify Lyrics Viewer is a tool that allows you to view the lyrics of the current playing song on Spotify by simply signing in.</p>
            </div>
        """
    ),
    FeaturedPost(type='post', post='how-to-hash-passwords-in-python'),
    FeaturedPost(type='post', post='how-to-make-hotkeys-in-python'),
]

redirects: Dict[str, str] = {
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
    'blog/post/who-is-on-my-network': 'blog/post/whos-on-my-network',
    'blog/post/how-to-serve-react-from-a-python-server': 'blog/post/how-to-serve-a-react-app-from-a-python-server'
}


# Validate home featured posts
for tile in featured_posts:
    assert tile.post != ''

    if tile.type == 'post-image':
        pass
    elif tile.type == 'post':
        pass
    elif tile.type == 'raw':
        assert tile.content is not None
    else:
        raise Exception(f"Unexpected home tile type: {tile.type}")
