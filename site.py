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
from collections import defaultdict
import string

import config


# Renderer


def my_renderer(text):
    pre_rendered_body = render_template_string(text)
    return markdown.markdown(pre_rendered_body, extensions=FLATPAGES_MARKDOWN_EXTENSIONS)


# Statics


# Flat pages and freezing
FLATPAGES_AUTO_RELOAD = config.get('serve-and-build', 'flatpages', 'debug')
FLATPAGES_EXTENSION = config.get('serve-and-build', 'flatpages', 'extension')
FLATPAGES_ROOT = config.get('serve-and-build', 'flatpages', 'root')
FLATPAGES_MARKDOWN_EXTENSIONS = config.get('serve-and-build', 'flatpages', 'markdown-extensions')
FLATPAGES_HTML_RENDERER = my_renderer

# Pagination
PAGINATION_PAGE_MAX = config.get('serve-and-build', 'pagination', 'max-per-page')
PAGINATION_EITHER_SIDE = config.get('serve-and-build', 'pagination', 'pages-either-side-in-nav')

# Paths
FREEZER_DESTINATION = config.get('serve-and-build', 'paths', 'build-destination')
ASSETS_LOCATION = config.get('serve-and-build', 'paths', 'assets')
POST_ASSETS_LOCATION = config.get('serve-and-build', 'paths', 'post-assets')

# Site specific
SITE = config.get('site')
REDIRECTS = config.get('redirects')
HOME_TILES = config.get('home-tiles')

# Get latest YouTube Videos (made the images static - no dynamic calls)
requested_videos = requests.get(
    'https://www.googleapis.com/youtube/v3/search?key=' + SITE['youtube_data_api_key'] + '&channelId=' + SITE['youtube_channel_id'] + '&part=id&order=date&maxResults=6&type=video'
).json()['items']

recent_videos = []
for video in requested_videos:
    if 'videoId' not in video['id']:
        continue
    recent_videos.append({
        'thumb_src': 'https://img.youtube.com/vi/' + video['id']['videoId'] + '/mqdefault.jpg',
        'href': 'https://www.youtube.com/watch?v=' + video['id']['videoId']
    })


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
    categories = defaultdict(list)
    for post in get_posts():
        category = post.meta.get('category', 'General')
        categories[category].append(post)
    return {t: categories[t] for t in sorted(categories)}


def posts_by_tag():
    """ Get posts by tag : {tag: [post, post, ...]} """
    tags = defaultdict(list)
    for post in get_posts():
        post_tags = post.meta.get('tags', [])
        for tag in post_tags:
            tags[tag].append(post)
    posts_by_tag_unsorted = {t: tags[t] for t in sorted(tags)}
    return dict(sorted(posts_by_tag_unsorted.items()))


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
    return render_template('about.html', build=os.getenv('build', 'Not Specified'))


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
        file_location = os.path.join(FLATPAGES_ROOT, post.path + '.md')
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


@app.route('/ads.txt')
def ads_txt():
    return 'google.com, {0}, DIRECT, f08c47fec0942fa0'.format(SITE['google_adsense_publisher_id'])


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


@app.context_processor
def inject_recent_videos():
    return dict(recent_videos=recent_videos)


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
        file_path = os.path.join(FREEZER_DESTINATION, r)
        file = os.path.join(file_path, 'index.html')
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
    f = open(os.path.join(FREEZER_DESTINATION, 'CNAME'), 'w')
    f.write(SITE['domain'])
    f.close()
    print('Added CNAME')

    # Add 404 page
    f = open(os.path.join(FREEZER_DESTINATION, '404.html'), 'w')
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

    tags = input('Tags (separated by comma): ').lower()

    post_id = quote_plus(''.join(
        [i for i in title.lower().replace(' ', '-') if i in string.ascii_letters + string.digits + '-']
    ))
    print('Post Id: {0}'.format(post_id))

    # Write file
    filename = post_id + '.md'
    file_path = os.path.join(FLATPAGES_ROOT, filename)
    f = open(file_path, 'w')
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
    print('\nCreated {0}'.format(file_path))

    # Create assets folder and add feature
    post_assets_location = os.path.join(POST_ASSETS_LOCATION, post_id)
    if not os.path.isdir(post_assets_location):
        os.makedirs(post_assets_location)
        print('Created: {0}'.format(post_assets_location))
    feature_img = os.path.join(POST_ASSETS_LOCATION, post_id, 'feature.png')
    if not os.path.isfile(feature_img):
        shutil.copyfile(
            os.path.join(ASSETS_LOCATION, 'img', 'default-feature.png'),
            feature_img
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
    os.environ['build'] = 'Development'
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
