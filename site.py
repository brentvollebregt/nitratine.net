import time
import os
import math
import markdown
import socket
from flask import Flask, render_template, send_from_directory, abort, render_template_string, url_for, redirect
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import requests
import argparse
from urllib.parse import quote_plus
import subprocess
import shutil


# Renderer


def my_renderer(text):
    pre_rendered_body = render_template_string(text)
    return markdown.markdown(pre_rendered_body, extensions=FLATPAGES_MARKDOWN_EXTENSIONS)


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

ASSETS_LOCATION = 'assets'
POST_ASSETS_LOCATION = 'post-assets'


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
    'title': 'Nitratine',
    'url': 'https://nitratine.net',
    'domain': 'nitratine.net',
    'about': 'Owner of <a href="https://www.youtube.com/PyTutorials">PyTurorials</a> and creator of <a href="https://github.com/brentvollebregt/auto-py-to-exe">auto-py-to-exe</a>. I enjoy making quick tutorials for people new to particular topics in Python and  tools that help fix small things.',
    'theme_colour': '#343a40',
    'email': 'brent@nitratine.net',
    'youtube_link': 'https://www.youtube.com/PyTutorials',
    'github_username': 'brentvollebregt',
    'default_author': 'Brent Vollebregt',
    'disqus_shortname': 'nitratine',
    'google_analytics_id': 'UA-117153268-2',
    'google_ad_client': 'ca-pub-6407227183932047',
    'youtube_channel_name': 'PrivateSplat',
    'youtube_channel_id': 'UCesEknt3SRX9R9W_f93Tb7g',
    'youtube_data_api_key': 'AIzaSyDz6QJ7H1Ca575XwvKnO8Q4MVATUxLdHYM'
}
REDIRECTS = {
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
    'common-issues-when-using-auto-py-to-exe': 'blog/post/common-issues-when-using-auto-py-to-exe',
    'encryption-and-decryption-in-python': 'blog/post/encryption-and-decryption-in-python',
    'blog/post/common-issues-when-using-auto-py-to-exe': 'blog/post/issues-when-using-auto-py-to-exe'
}
HOME_TILES = [
    {
        'type': 'img-content',
        'link': 'https://github.com/brentvollebregt/auto-py-to-exe',
        'image_url': '/post-assets/auto-py-to-exe/feature.png',
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
        'post': 'issues-when-using-auto-py-to-exe',
        'reason': 'New'
    },
    {
        'type': 'post',
        'post': 'who-is-on-my-network',
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


def get_posts(hidden=False, force_post=None):
    """ Get all posts in order of date. Posts can be hidden. """
    all_posts = [p for p in posts if hidden or 'hidden' not in p.meta or force_post == p.path]
    all_posts.sort(key=lambda x: x.meta['date'], reverse=True)
    return all_posts


def posts_by_category():
    """ Get posts by category : {category: [post, post, ...]} """
    categories = {c: [] for c in CATEGORIES}
    for post in get_posts():
        category = post.meta.get('category', 'General')
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
    return {t: tags[t] for t in sorted(tags)}


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


def get_previous_and_next_posts(post):
    """ Get the next and previous post for a particular post """
    # So we don't call it over and over again
    all_posts = get_posts(force_post=post.path)

    # Find it's index
    title = post.meta['title']
    post_index = next((i for (i, d) in enumerate(all_posts) if d.meta['title'] == title), None)

    # Calculate next and previous
    prev_and_next = {}
    if post_index != 0:
        prev_and_next['next'] = all_posts[post_index - 1]
    else:
        prev_and_next['next'] = None
    if post_index < len(all_posts) - 1:
        prev_and_next['prev'] = all_posts[post_index + 1]
    else:
        prev_and_next['prev'] = None

    return prev_and_next


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
                tile['image_url'] = url_for(
                    'post_assets',
                    path=tile['post'] + '/' + page.meta.get('feature', 'INVALID')
                )
            else:
                tile['image_url'] = url_for(
                    'assets',
                    path='img/default-feature.png'
                )

    return render_template(
        'home.html',
        tiles=HOME_TILES
    )


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/portfolio/')
def portfolio():
    return render_template('portfolio.html')


@app.route('/data/')
def data():
    public_posts = get_posts()
    available_posts = [[p.path, p['title']] for p in public_posts]

    req = requests.get('https://api.github.com/users/' + SITE['github_username'] + '/repos')
    req_data = req.json()
    available_repos = sorted(
        [[i['full_name'], i['stargazers_count']] for i in req_data],
        key=lambda x: x[1],
        reverse=True
    )

    return render_template(
        'data.html',
        repos=available_repos,
        posts=available_posts
    )


@app.route('/search/')
def search():
    return render_template(
        'search.html',
        site_content={post.path: post.meta for post in get_posts()}
    )


@app.route('/blog/')
def blog_home():
    page1_posts = paginate_posts(1)
    pagination_nav_data = get_pagination_nav_data(1)
    return render_template(
        'blog-home.html',
        category_numbers=post_numbers_by_category(),
        pagination_nav=pagination_nav_data,
        posts=page1_posts
    )


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
    return render_template(
        'blog-home.html',
        category_numbers=post_numbers_by_category(),
        pagination_nav=pagination_nav_data,
        posts=pagen_posts
    )


@app.route('/blog/categories/')
def blog_categories():
    return render_template(
        'blog-categories.html',
        category_numbers=post_numbers_by_category(),
        categories=posts_by_category(),
        title='Categories'
    )


@app.route('/blog/tags/')
def blog_tags():
    return render_template(
        'blog-categories.html',
        category_numbers=post_numbers_by_category(),
        categories=posts_by_tag(),
        title='Tags'
    )


@app.route('/blog/archive/')
def blog_archive():
    return render_template(
        'blog-categories.html',
        category_numbers=post_numbers_by_category(),
        categories=posts_by_date(),
        title='Date'
    )


@app.route('/blog/post/<path:path>/')
def blog_post(path):
    page = posts.get_or_404(path)
    return render_template(
        'blog-post.html',
        category_numbers=post_numbers_by_category(),
        prev_and_next=get_previous_and_next_posts(page),
        page=page
    )


# Site Management Routes


@app.route('/sitemap.xml')
def sitemap():
    pages = []
    for post in get_posts():
        file_location = FLATPAGES_ROOT + post.path + '.md'
        pages.append({
            'loc': url_for('blog_post', path=post.path),
            'lastmod': time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(file_location)))
        })
    pages.append({'loc': url_for('index')})
    pages.append({'loc': url_for('about')})
    pages.append({'loc': url_for('portfolio')})
    pages.append({'loc': url_for('blog_home')})
    pages.append({'loc': url_for('blog_categories')})
    pages.append({'loc': url_for('blog_tags')})
    pages.append({'loc': url_for('blog_archive')})

    return render_template(
        'sitemap.xml',
        pages=pages
    )


@app.route('/<path:path>/')
def redirects(path):
    if path not in REDIRECTS:
        abort(404)
    redirect_to = '/' + REDIRECTS[path] + '/'
    return render_template(
        'redirect.html',
        redirect_to=redirect_to
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Asset Routes


# @app.route('/assets/css/pygments.css')
# def pygments_css():
#     return pygments_style_defs('native'), 200, {'Content-Type': 'text/css'}


@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory(ASSETS_LOCATION, path)


@app.route('/post-assets/<path:path>')
def post_assets(path):
    return send_from_directory(POST_ASSETS_LOCATION, path)


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
def blog_post():
    all_posts = get_posts(hidden=True)
    for post in all_posts:
        yield {'path': post.path}


@freezer.register_generator
def assets():
    location = ASSETS_LOCATION
    for root, dirs, files in os.walk(location, topdown=False):
        for name in files:
            # Get the root and remove the location plus \. Then replace any \ with / and add the file name
            yield {'path': root[len(location)+1:].replace('\\', '/') + '/' + name}


@freezer.register_generator
def post_assets():
    location = POST_ASSETS_LOCATION
    for root, dirs, files in os.walk(location, topdown=False):
        for name in files:
            yield {'path': root[len(location)+1:].replace('\\', '/') + '/' + name}


# Argument functions


def build():
    print('Freezing')
    freezer.freeze()

    # Create redirects (because Frozen-Flask doesn't have an option)
    for r in REDIRECTS:
        file_path = FREEZER_DESTINATION + '/' + r
        file = file_path + '/index.html'
        # Check where we are writing
        if os.path.exists(file):
            print('WARN: Overwriting ' + file_path)
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        # Write redirect
        f = open(file, 'w')
        with app.app_context():
            f.write(redirects(path=r))
        f.close()
    print('Added Redirects')

    # Add CNAME
    f = open(FREEZER_DESTINATION + '/CNAME', 'w')
    f.write(SITE['domain'])
    f.close()
    print('Added CNAME')

    # Add 404 page
    f = open(FREEZER_DESTINATION + '/404.html', 'w')
    with app.test_request_context():
        f.write(page_not_found(None)[0])
    f.close()
    print('Added 404')


def new_post():
    print('New post will be saved to {0}'.format(FLATPAGES_ROOT))
    title = input('Title: ')
    date = time.strftime('%Y-%m-%d')

    # Category selection
    while True:
        print('Select a category from the following list by its index')
        categories = [i for i in posts_by_category()]
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

    tags = input('Tags (separated by comma): ')

    post_id = quote_plus(title.lower().replace(' ', '-'))
    print('Post Id: {0}'.format(post_id))

    # Write file
    filename = post_id + '.md'
    f = open(FLATPAGES_ROOT + filename, 'w')
    f.write('title: "{0}"\n'.format(title))
    f.write('date: {0}\n'.format(date))
    f.write('category: {0}\n'.format(category))
    f.write('tags: [{0}]\n'.format(tags))
    f.write('feature: feature.png\n')
    f.write('description: ""\n')
    f.write('\n[TOC]\n')
    f.write('\n## Content\n')
    f.write("{% with video_id=\"XXXXXXXXXXX\" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}")
    f.close()
    print('\nCreated {0}'.format(FLATPAGES_ROOT + filename))

    # Create assets folder and add feature
    post_assets_location = POST_ASSETS_LOCATION + '/' + post_id + '/'
    if not os.path.isdir(post_assets_location):
        os.makedirs(post_assets_location)
        print('Created: {0}'.format(post_assets_location))
    feature_img = POST_ASSETS_LOCATION + '/' + post_id + '/feature.png'
    if not os.path.isfile(feature_img):
        shutil.copyfile(
            ASSETS_LOCATION + '/img/default-feature.png',
            POST_ASSETS_LOCATION + '/' + post_id + '/feature.png'
        )
        print('Created: {0}'.format(feature_img))


def serve_build():
    process = None
    try:
        process = subprocess.Popen(
            'python -m http.server',
            cwd=FREEZER_DESTINATION,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print('http://{0}:8000'.format(socket.gethostbyname(socket.gethostname())))
        input('Press enter to stop the server')
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if process is not None:
            process.terminate()


def run():
    print('WARN: This server is designed to be used in production')
    app.run(port=8000, host=socket.gethostbyname(socket.gethostname()))


# On Execution


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to run and build nitratine.net')
    parser.add_argument('-b', '--build', action="store_true", default=False, help='Build site to static files')
    parser.add_argument('-n', '--new-post', action="store_true", default=False, help='Create a new post')
    parser.add_argument('-s', '--serve-build', action="store_true", default=False, help='Serve the built site')
    args = parser.parse_args()

    if args.build:
        build()
    elif args.new_post:
        new_post()
    elif args.serve_build:
        serve_build()
    else:
        run()
