import sys
import time
import os
import math
import markdown
import socket
from flask import Flask, render_template, send_from_directory, abort, render_template_string, url_for
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import requests


# Renderer

def my_renderer(text):
    prerendered_body = render_template_string(text)
    return markdown.markdown(prerendered_body, extensions=FLATPAGES_MARKDOWN_EXTENSIONS)


# Statics

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'posts/'
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'extra', 'toc']
FLATPAGES_HTML_RENDERER = my_renderer
FREEZER_DESTINATION = 'docs'
PAGINATION_PAGE_MAX = 10
PAGINATION_EITHER_SIDE = 2


# Specific Site Statics

CATEGORIES = [
    'YouTube',
    'Projects',
    'Tutorials',
    'Apps',
    'Investigations',
    'General'
]
SITE = {
    'title' : 'Nitratine',
    'url' : 'https://nitratine.net',
    'domain': 'nitratine.net',
    'about' : 'Owner of <a href="https://www.youtube.com/PyTutorialsOriginal">PyTurorials</a> and creator of <a href="https://github.com/brentvollebregt/auto-py-to-exe">auto-py-to-exe</a>. I enjoy making quick tutorials for people new to particular topics in Python and  tools that help fix small things.',
    'theme_colour' : '#343a40',
    'email' : 'brent@nitratine.net',
    'youtube_link' : 'https://www.youtube.com/PyTutorialsOriginal',
    'github_username' : 'brentvollebregt',
    'default_author' : 'Brent Vollebregt',
    'disqus_shortname' : 'nitratine',
    'google_analytics_id' : 'UA-117153268-2',
    'google_ad_client' : 'ca-pub-6407227183932047',
    'youtube_channel_name' : 'PrivateSplat',
    'youtube_channel_id' : 'UCesEknt3SRX9R9W_f93Tb7g',
    'youtube_data_api_key' : 'AIzaSyDz6QJ7H1Ca575XwvKnO8Q4MVATUxLdHYM'
}
REDIRECTS = {
    'donations' : 'about',
    'blog/post' : 'blog',
    'colour' : 'blog/post/colour',
    'finding-emotion-in-music-with-python' : 'blog/post/finding-emotion-in-music-with-python',
    'interesting-sites' : 'blog/post/interesting-sites',
    'randomly-generating-numbers-to-fulfil-an-integer-range' : 'blog/post/randomly-generating-numbers-to-fulfil-an-integer-range',
    'convert-py-to-exe' : 'blog/post/convert-py-to-exe',
    'get-wifi-passwords-with-python' : 'blog/post/get-wifi-passwords-with-python',
    'how-to-setup-pythons-pip' : 'blog/post/how-to-setup-pythons-pip',
    'how-to-get-mouse-clicks-with-python' : 'blog/post/how-to-get-mouse-clicks-with-python',
    'python-keylogger' : 'blog/post/python-keylogger',
    'simulate-keypresses-in-python' : 'blog/post/simulate-keypresses-in-python',
    'quick-script' : 'blog/post/quick-script',
    'lucy-in-the-sky-with-emotion' : 'blog/post/lucy-in-the-sky-with-emotion',
    'monopoly-money' : 'blog/post/monopoly-money',
    'mp3-itunes-downloader' : 'blog/post/mp3-itunes-downloader',
    'spotify-playlist-downloader' : 'blog/post/spotify-playlist-downloader',
    'adding-snow-to-your-website' : 'blog/post/adding-snow-to-your-website',
    'change-file-modification-time-in-python' : 'blog/post/change-file-modification-time-in-python',
    'the-nitratine-project' : 'blog/post/the-nitratine-project',
    'how-to-make-hotkeys-in-python' : 'blog/post/how-to-make-hotkeys-in-python',
    'simulate-mouse-events-in-python' : 'blog/post/simulate-mouse-events-in-python',
    'how-to-send-an-email-with-python' : 'blog/post/how-to-send-an-email-with-python',
    'python-retweet-bot' : 'blog/post/python-retweet-bot',
    'python-auto-clicker' : 'blog/post/python-auto-clicker',
    'auto-py-to-exe' : 'blog/post/auto-py-to-exe',
    'hit-counter' : 'blog/post/hit-counter',
    'github-badges' : 'blog/post/github-badges',
    'my-desktop-backgrounds' : 'blog/post/my-desktop-backgrounds',
    'how-to-add-a-custom-domain-to-a-github-pages-site' : 'blog/post/how-to-add-a-custom-domain-to-a-github-pages-site',
    'python-threading-basics' : 'blog/post/python-threading-basics',
    'python-gui-using-chrome' : 'blog/post/python-gui-using-chrome',
    'python-sqlite3-basics' : 'blog/post/python-sqlite3-basics',
    'price-per-unit' : 'blog/post/price-per-unit',
    'putting-auto-py-to-exe-on-pypi' : 'blog/post/putting-auto-py-to-exe-on-pypi',
    'media-picker' : 'blog/post/media-picker',
    'python-guis-with-pyqt' : 'blog/post/python-guis-with-pyqt',
    'how-to-clean-a-twitter-account-with-jquery' : 'blog/post/how-to-clean-a-twitter-account-with-jquery',
    'multi-clipboard' : 'blog/post/multi-clipboard',
    'uow-moodle-rwa-ignorer' : 'blog/post/uow-moodle-rwa-ignorer',
    'am-i-a-participant' : 'blog/post/am-i-a-participant',
    'asymmetric-encryption-and-decryption-in-python' : 'blog/post/asymmetric-encryption-and-decryption-in-python',
    'common-issues-when-using-auto-py-to-exe' : 'blog/post/common-issues-when-using-auto-py-to-exe',
    'encryption-and-decryption-in-python' : 'blog/post/encryption-and-decryption-in-python'
}
HOME_TILES = [
    {
        'type': 'img-content',
        'link': 'https://github.com/brentvollebregt/auto-py-to-exe',
        'image_url': 'https://i.imgur.com/dd0LC2n.png',
        'content_raw': '<div class="text-center"> <h5 class="card-title mb-1">Auto Py to Exe</h5> <img alt="Total downloads for auto-py-to-exe project" src="https://pepy.tech/badge/auto-py-to-exe"> <br> <small class="text-muted">pip install auto-py-to-exe</small> </div>'
    },
    {
        'type': 'image',
        'link': 'https://youtu.be/H8t4DJ3Tdrg',
        'image_url': 'https://img.youtube.com/vi/H8t4DJ3Tdrg/mqdefault.jpg'
    },
    {
        'type': 'post',
        'post': 'asymmetric-encryption-and-decryption-in-python',
        'reason': 'New'
    },
    {
        'type': 'image',
        'link': 'https://youtu.be/ksW59gYEl6Q',
        'image_url': 'https://img.youtube.com/vi/ksW59gYEl6Q/mqdefault.jpg'
    },
    {
        'type': 'image',
        'link': 'https://youtu.be/YPiHBtddefI',
        'image_url': 'https://img.youtube.com/vi/YPiHBtddefI/mqdefault.jpg'
    },
    {
        'type': 'post',
        'post': 'common-issues-when-using-auto-py-to-exe',
        'reason': 'New'
    },
    {
        'type': 'post',
        'post': 'encryption-and-decryption-in-python',
        'reason': 'New'
    },
    {
        'type': 'post',
        'post': 'get-wifi-passwords-with-python',
        'reason': 'Popular'
    },
    {
        'type': 'image',
        'link': 'https://youtu.be/OZSZHmWSOeM',
        'image_url': 'https://img.youtube.com/vi/OZSZHmWSOeM/mqdefault.jpg'
    },
    {
        'type': 'post',
        'post': 'python-keylogger',
        'reason': 'Popular'
    },
    {
        'type': 'post',
        'post': 'python-threading-basics',
        'reason': 'Popular'
    },
    # {
    #     'type': 'image',
    #     'link': '',
    #     'image_url': ''
    # },
    # {
    #     'type': 'post',
    #     'post': '',
    #     'reason': 'popular/new'
    # },
    # {
    #     'type': 'img-content',
    #     'link': '',
    #     'image_url': '',
    #     'content_raw': ''
    # },
    # {
    #     'type': 'raw',
    #     'link': '',
    #     'content': ''
    # }
]


# App instances

app = Flask(__name__)
app.config.from_object(__name__)
posts = FlatPages(app)
freezer = Freezer(app)


# Helpers

def get_posts():
    """ Get all vaiable posts in order of date """
    all_posts = [p for p in posts]
    all_posts.sort(key=lambda x: x.meta['date'], reverse=True)
    return all_posts

def posts_by_category():
    """ Get posts by category : {category: [post, post, ...]} """
    categories = {c: [] for c in CATEGORIES}
    for post in get_posts():
        category = post.meta.get('categories', 'General')
        categories[category].append(post)
    return categories

def posts_by_tag():
    """ Get posts by tag : {tag: [post, post, ...]} """
    tags = {}
    for post in get_posts():
        post_tags = post.meta.get('tags', [])
        for tag in post_tags:
            if tag in tags:
                tags[tag].append(post)
            else:
                tags[tag] = [post]
    return {t:tags[t] for t in sorted(tags)}

def posts_by_date():
    """ Get posts by year : {year: [post, post, ...]} """
    years = {}
    for post in get_posts():
        post_date = post.meta.get('date', '1970-01-01')
        struct_time = time.strptime(str(post_date), '%Y-%m-%d')
        year = str(struct_time.tm_year)
        if year not in years:
            years[year] = [post]
        else:
            years[year].append(post)
    return years

def post_numbers_by_category():
    """ Get number of posts per category : {category: count} """
    categories = posts_by_category()
    return {c: len(categories[c]) for c in categories}

def chunk_list(l, n):
    """ Yield successive n-sized chunks from l. """
    for i in range(0, len(l), n):
        yield l[i:i + n]

def paginate_posts(page):
    """ Get posts for a particular page """
    page = page - 1 # Adjust to start a 0
    chunked_posts = list(chunk_list(get_posts(), PAGINATION_PAGE_MAX))
    if page > len(chunked_posts) - 1:
        return []
    return chunked_posts[page]

def available_pagination_pages():
    """ Get the available pages """
    chunked_posts = list(chunk_list(get_posts(), PAGINATION_PAGE_MAX))
    return [i for i in range(1, len(chunked_posts) + 1)]

def get_pagination_nav_data(page):
    """ Calculate pages to show in navigation """
    available_pages = available_pagination_pages()

    # Calculate pagination nav
    minimum = 1
    total = len(available_pages)
    length = 1 + (PAGINATION_EITHER_SIDE * 2)
    if length > total:
        length = total
    start = page - math.floor(length / 2)
    start = max(start, minimum)
    start = min(start, minimum + total - length)

    navigation = {
        'next': page + 1 if page + 1 in available_pages else None,
        'prev': page - 1 if page - 1 in available_pages else None,
        'current': page,
        'pages': [i for i in range(start, start + length)]
    }
    return navigation


# Page Routes

@app.route('/')
def index():
    for tile in HOME_TILES:
        if tile['type'] == 'post':
            page = posts.get(tile['post'])
            tile['link'] = url_for('blog_post', path=tile['post'])
            tile['title'] = page.meta.get('title', 'INVALID')
            tile['text'] = page.meta.get('description', 'INVALID')
            tile['date'] = ymd_format(page.meta.get('date', 'INVALID'))
            if 'feature' in page.meta:
                tile['image_url'] = 'post-assets/' + tile['post'] + '/' + page.meta.get('feature', 'INVALID')
            else:
                tile['image_url'] = 'assets/img/default-feature.png'

    return render_template('home.html', tiles=HOME_TILES)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/portfolio/')
def portfolio():
    return render_template('portfolio.html')

@app.route('/data/')
def data():
    available_posts = [[i, posts._pages[i]['title']] for i in posts._pages]

    req = requests.get('https://api.github.com/users/' + SITE['github_username'] + '/repos')
    req_data = req.json()
    available_repos = sorted([[i['full_name'], i['stargazers_count']] for i in req_data], key=lambda x: x[1], reverse=True)

    return render_template('data.html', repos=available_repos, posts=available_posts)

@app.route('/blog/')
def blog_home():
    page1_posts = paginate_posts(1)
    pagination_nav_data = get_pagination_nav_data(1)
    return render_template('blog-home.html', category_numbers=post_numbers_by_category(), pagination_nav=pagination_nav_data, posts=page1_posts)

@app.route('/blog/page/<int:page>/')
def blog_pagination(page):
    if page == 1:
        return redirect(url_for('blog_home'))
    if page < 1:
        abort(404)
    pagen_posts = paginate_posts(page)
    if not pagen_posts:
        abort(404)
    pagination_nav_data = get_pagination_nav_data(page)
    return render_template('blog-home.html', category_numbers=post_numbers_by_category(), pagination_nav=pagination_nav_data, posts=pagen_posts)

@app.route('/blog/categories/')
def blog_categories():
    return render_template('blog-categories.html', category_numbers=post_numbers_by_category(), categories=posts_by_category(), title='Categories')

@app.route('/blog/tags/')
def blog_tags():
    return render_template('blog-categories.html', category_numbers=post_numbers_by_category(), categories=posts_by_tag(), title='Tags')

@app.route('/blog/archive/')
def blog_archive():
    return render_template('blog-categories.html', category_numbers=post_numbers_by_category(), categories=posts_by_date(), title='Date')

@app.route('/blog/post/<path:path>/')
def blog_post(path):
    page = posts.get_or_404(path)
    return render_template('blog-post.html', category_numbers=post_numbers_by_category(), page=page)


# Site Management Routes

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    for post in get_posts():
        file_location = FLATPAGES_ROOT + post.path + '.md'
        pages.append({
            'loc' : url_for('blog_post', path=post.path),
            'lastmod' : time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(file_location)))
        })
    pages.append({'loc': url_for('index')})
    pages.append({'loc': url_for('about')})
    pages.append({'loc': url_for('portfolio')})
    pages.append({'loc': url_for('blog_home')})
    pages.append({'loc': url_for('blog_categories')})
    pages.append({'loc': url_for('blog_tags')})
    pages.append({'loc': url_for('blog_archive')})

    return render_template('sitemap.xml', pages=pages)

@app.route('/<path:path>/')
def redirects(path):
    if path not in REDIRECTS:
        abort(404)
    redirect_to = '/' + REDIRECTS[path] + '/'
    return render_template('redirect.html', redirect_to=redirect_to)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Asset Routes

# @app.route('/assets/css/pygments.css')
# def pygments_css():
#     return pygments_style_defs('native'), 200, {'Content-Type': 'text/css'}

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('assets', path)

@app.route('/post-assets/<path:path>')
def post_assets(path):
    return send_from_directory('post-assets', path)


# Injectors

@app.context_processor
def inject_site():
    return dict(site=SITE)

def ymd_format(date):
    """ Convert 2018-10-30 to 30 Nov 2018 """
    struct_time = time.strptime(str(date), '%Y-%m-%d')
    return time.strftime('%d %b %Y', struct_time)

app.jinja_env.globals.update(ymd_format=ymd_format)


# Build Generators

@freezer.register_generator
def assets():
    location = "assets/"
    for root, dirs, files in os.walk(location, topdown=False):
        for name in files:
            yield {'path': root[len(location):].replace('\\', '/') + '/' +  name}

@freezer.register_generator
def post_assets():
    location = "post-assets/"
    for root, dirs, files in os.walk(location, topdown=False):
        for name in files:
            print(os.path.join(root, name))
            yield {'path': root[len(location):].replace('\\', '/') + '/' +  name}


# On Execution

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()

        # Create redirects (because Frozen-Flask doesn't have an option)
        for redirect in REDIRECTS:
            path = FREEZER_DESTINATION + '/' + redirect
            file = path + '/index.html'
            if os.path.exists(file):
                print ('WARN: Overwirting ' + path)
            if not os.path.isdir(path):
                os.makedirs(path)
            f = open(file, 'w')
            with app.app_context():
                f.write(redirects(path=redirect))
            f.close()

        # Add CNAME
        f = open(FREEZER_DESTINATION + '/CNAME', 'w')
        f.write(SITE['domain'])
        f.close()

        # Add 404 page
        f = open(FREEZER_DESTINATION + '/404.html', 'w')
        with app.test_request_context():
            f.write(page_not_found(None)[0])
        f.close()

    else:
        print ('WARN: This server is designed to be used in production')
        app.run(port=8000, host=socket.gethostbyname(socket.gethostname()))
