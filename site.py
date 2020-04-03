import time
import os
import math
import socket
import argparse
from urllib.parse import quote_plus
import subprocess
from collections import defaultdict
import string

from config import config
import external

import markdown
from flask import Flask, render_template, send_from_directory, abort, render_template_string, url_for, redirect
from flask_flatpages import FlatPages
from flask_frozen import Freezer


# Renderer


def my_renderer(text):
    pre_rendered_body = render_template_string(text)
    return markdown.markdown(pre_rendered_body, extensions=FLATPAGES_MARKDOWN_EXTENSIONS)


# Statics


# Flat pages and freezing (documented at https://pythonhosted.org/Flask-FlatPages/#configuration)
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'posts'
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'extra', 'toc']
FLATPAGES_HTML_RENDERER = my_renderer

# Pagination
PAGINATION_PAGE_MAX = 10 # Max amount of posts per page
PAGINATION_EITHER_SIDE = 2 # Number of tiles beside current tile/page in pagination navigation e.g. 2 = P P C N N

# Paths
FREEZER_DESTINATION = 'build' # Build location
ASSETS_LOCATION = 'assets' # Site assets location
POST_FILENAME = 'post'  # The name of the .md files used as the post page

# Get latest YouTube Videos (made the images static - no dynamic calls)
recent_youtube_videos = external.get_most_recent_youtube_videos(
    youtube_data_api_key=config.site.youtube_data_api_key,
    youtube_channel_id=config.site.youtube_channel_id,
    max_results=6
)

# Get GitHub repository stats
github_user_repos = external.get_github_user_repos(
    github_username=config.site.github_username
)


# App instance


app = Flask(__name__)
app.config.from_object(__name__)
posts = FlatPages(app)
freezer = Freezer(app)


# Helpers


def get_posts(hidden=False, force_post=None):
    """ Get all posts in order of date.
    :param hidden: Whether to return hidden posts or not
    :param force_post: Whether to return a particular post no matter what (is used so hidden posts can see themselves in prev/next calculations)
    :return: Available posts
    """
    all_posts = [p for p in posts if hidden or 'hidden' not in p.meta or force_post == p.path]
    all_posts.sort(key=lambda x: x.meta['date'], reverse=True)
    for post in all_posts:
        post.path = post.path.replace(f'/{POST_FILENAME}', '')
    return all_posts


def posts_by_category():
    """ Get posts by category
    :return: {category: [post, post, ...]}
    """
    categories = defaultdict(list)
    for post in get_posts():
        category = post.meta.get('category', 'General')
        categories[category].append(post)
    return {t: categories[t] for t in sorted(categories)}


def posts_by_tag():
    """ Get posts by tag
    :return: {tag: [post, post, ...]}
    """
    tags = defaultdict(list)
    for post in get_posts():
        post_tags = post.meta.get('tags', [])
        for tag in post_tags:
            tags[tag].append(post)
    posts_by_tag_unsorted = {t: tags[t] for t in sorted(tags)}
    return dict(sorted(posts_by_tag_unsorted.items()))


def posts_by_date():
    """ Get posts by year
    :return: {year: [post, post, ...]}
    """
    years = defaultdict(list)
    for post in get_posts():
        post_date = post.meta.get('date', '1970-01-01')
        struct_time = time.strptime(str(post_date), '%Y-%m-%d')
        year = str(struct_time.tm_year)
        years[year].append(post)
    return years


def post_numbers_by_category():
    """ Get number of posts per category
    :return: {category: count}
    """
    categories = posts_by_category()
    return {c: len(categories[c]) for c in categories}


def chunk_list(l, n):
    """ Yield successive n-sized chunks from l. src: https://stackoverflow.com/a/312464 """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def paginate_posts(page):
    """ Get posts for a particular page
    :param page: The page number (0-indexed)
    :return: A list of posts on this page
    """
    page = page - 1 # Adjust to start a 0
    chunked_posts = list(chunk_list(get_posts(), PAGINATION_PAGE_MAX))
    if page > len(chunked_posts) - 1:
        return []
    return chunked_posts[page]


def available_pagination_pages():
    """ Get the available pages
    :return: A list of page numbers that are available
    """
    chunked_posts = list(chunk_list(get_posts(), PAGINATION_PAGE_MAX))
    return list(range(1, len(chunked_posts) + 1))


def get_pagination_nav_data(page):
    """ Calculate pages to show in navigation
    :param page: The page to get navigation data for
    :return: An object to create the pagination buttons
    """
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
    """ Get the next and previous post for a particular post
    :param post: The post to get the previous and next post for
    :return: The previous and next post (either could be None)
    """
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
    """ The home page """
    for tile in config.home_tiles:
        if tile['type'] == 'post':
            page = posts.get(tile['post'] + f'/{POST_FILENAME}')
            tile['link'] = url_for('blog_post', path=tile['post'])
            tile['title'] = page.meta.get('title', 'INVALID')
            tile['text'] = page.meta.get('description', 'INVALID')
            tile['date'] = ymd_format(page.meta.get('date', 'INVALID'))
            tile['image_url'] = url_for(
                'post_assets',
                path=f'{tile["post"]}/{page.meta.get("feature", "INVALID")}'
            )
        elif tile['type'] == 'post-image':
            tile['link'] = url_for('blog_post', path=tile['post'])

    return render_template(
        'home.html',
        tiles=config.home_tiles
    )


@app.route('/about/')
def about():
    """ The about page """
    build_version = os.getenv('BUILD_VERSION', 'Unspecified')
    if build_version == 'production':  # Add date to production builds
        build_version += f" ({time.strftime('%d/%m/%Y %H:%M:%S')})"
    return render_template('about.html', build=build_version)


@app.route('/portfolio/')
def portfolio():
    """ The portfolio page """
    return render_template('portfolio.html')


@app.route('/data/')
def data():
    """ The data page """
    public_posts = get_posts()
    available_posts = [[p.path, p['title']] for p in public_posts]

    return render_template(
        'data.html',
        repos=github_user_repos,
        posts=available_posts
    )


@app.route('/search/')
def search():
    """ The search page """
    return render_template(
        'search.html',
        site_content=[{'meta': post.meta, 'path': post.path} for post in get_posts()]
    )


@app.route('/blog/')
def blog_home():
    """ Page 1 of the blog feed """
    page1_posts = paginate_posts(1)
    return render_template(
        'blog-home.html',
        category_numbers=post_numbers_by_category(),
        pagination_nav=get_pagination_nav_data(1),
        posts=page1_posts
    )


@app.route('/blog/page/<int:page>/')
def blog_pagination(page):
    """ Page n of the blog feed (or 404 if the page does not exist) """
    if page == 1:
        return redirect(url_for('blog_home'))
    if page < 1:
        abort(404)
    pagen_posts = paginate_posts(page)
    if not pagen_posts:
        abort(404)
    return render_template(
        'blog-home.html',
        category_numbers=post_numbers_by_category(),
        pagination_nav=get_pagination_nav_data(page),
        posts=pagen_posts
    )


@app.route('/blog/categories/')
def blog_categories():
    """ Posts grouped by categories """
    return render_template(
        'blog-categories.html',
        category_numbers=post_numbers_by_category(),
        categories=posts_by_category(),
        title='Categories',
        sort_type='category'
    )


@app.route('/blog/tags/')
def blog_tags():
    """ Posts grouped by tags """
    return render_template(
        'blog-categories.html',
        category_numbers=post_numbers_by_category(),
        categories=posts_by_tag(),
        title='Tags',
        sort_type='tag'
    )


@app.route('/blog/archive/')
def blog_archive():
    """ Posts grouped and sorted by date """
    return render_template(
        'blog-categories.html',
        category_numbers=post_numbers_by_category(),
        categories=posts_by_date(),
        title='Date',
        sort_type='date'
    )


@app.route('/blog/post/<path:path>/')
def blog_post(path):
    """ A post. Renders the .md file. """
    page = posts.get_or_404(f'{path}/{POST_FILENAME}')
    return render_template(
        'blog-post.html',
        category_numbers=post_numbers_by_category(),
        prev_and_next=get_previous_and_next_posts(page),
        page=page
    )


# Site Management Routes


@app.route('/sitemap.xml')
def sitemap():
    """ The XML sitemap """
    pages = []
    for post in get_posts():
        file_location = os.path.join(FLATPAGES_ROOT, post.path, f'{POST_FILENAME}.md')
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
    """ An easy way to generate ads.txt """
    return 'google.com, {0}, DIRECT, f08c47fec0942fa0'.format(config.site.google_adsense_publisher_id)


@app.route('/assets/<path:path>')
def assets(path):
    """ Calls for files in the asset location """
    return send_from_directory(ASSETS_LOCATION, path)


@app.route('/posts/<path:path>')
def post_assets(path):
    """ Calls for post assets. Technically this could return the post .md file but this has been disabled. """
    if path.endswith(f'/{POST_FILENAME}.md'):
        abort(403)  # This file is not meant to be accessible from this route
    return send_from_directory(FLATPAGES_ROOT, path)


@app.route('/<path:path>/')
def redirects(path):
    """ Catches any routes not handled by the previous functions. Used to identify potential redirects. """
    if path not in config.redirects:
        abort(404)
    redirect_to = f'/{config.redirects[path]}/'
    return render_template(
        'redirect.html',
        redirect_to=redirect_to
    )


@app.errorhandler(404)
def page_not_found(e):
    """ The page to display on a 404 """
    return render_template('404.html'), 404


# Injectors


@app.context_processor
def inject_site():
    """ Provide site_config to Jinja templates """
    return dict(site_config=config.site)


@app.context_processor
def inject_recent_videos():
    """ Provide recent_videos to Jinja templates """
    return dict(recent_videos=recent_youtube_videos)


def ymd_format(date):
    """ Convert 2018-10-30 to 30 Nov 2018 """
    struct_time = time.strptime(str(date), '%Y-%m-%d')
    return time.strftime('%d %b %Y', struct_time)


app.jinja_env.globals.update(ymd_format=ymd_format)  # Allow ymd_format to be called in a Jinja template


# Build Generators


@freezer.register_generator
def blog_post():
    """ Freezer function to identify all posts """
    all_posts = get_posts(hidden=True)
    for post in all_posts:
        print(f'Post: {post.path}')
        yield {'path': post.path}


@freezer.register_generator
def assets():
    """ Freezer function to identify all assets """
    location = ASSETS_LOCATION
    for root, dirs, files in os.walk(location, topdown=False):
        for name in files:
            path_in_location = root[len(location)+1:].replace('\\', '/') + '/' + name
            print(f'Asset: {ASSETS_LOCATION}/{name}')
            yield {'path': path_in_location}


@freezer.register_generator
def post_assets():
    """ Freezer function to identify all post assets (not the post .md file) """
    location = FLATPAGES_ROOT
    for root, dirs, files in os.walk(location, topdown=False):
        for name in files:
            if name == f'{POST_FILENAME}.md':
                continue  # No need to freeze this file
            path_in_location = root[len(location) + 1:].replace('\\', '/') + '/' + name
            print(f'Post Asset: {FLATPAGES_ROOT}/{path_in_location}')
            yield {'path': path_in_location}


# Argument functions


def build():
    """ Build the site and dump it in FREEZER_DESTINATION """
    print('Freezing')
    freezer.freeze()

    # Create redirects (because Frozen-Flask doesn't have an option)
    for r in config.redirects:
        file_path = os.path.join(FREEZER_DESTINATION, r)
        file = os.path.join(file_path, 'index.html')
        # Check where we are writing
        if os.path.exists(file):
            print(f'WARN: Overwriting {file_path}')
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        # Write redirect
        f = open(file, 'w')
        with app.app_context():
            f.write(redirects(path=r))
        f.close()
        print(f'Redirect: /{r}')

    # Add CNAME
    f = open(os.path.join(FREEZER_DESTINATION, 'CNAME'), 'w')
    f.write(config.site.domain)
    f.close()
    print('CNAME')

    # Add 404 page
    f = open(os.path.join(FREEZER_DESTINATION, '404.html'), 'w')
    with app.test_request_context():
        f.write(page_not_found(None)[0])
    f.close()
    print('404.html')


def new_post():
    """ Automatically setup a new posts file structure """
    title = input('Title: ')
    post_id = quote_plus(''.join(
        [i for i in title.lower().replace(' ', '-') if i in f'{string.ascii_letters}{string.digits}-']
    ))
    post_directory = os.path.join(FLATPAGES_ROOT, post_id)
    print('Post will be found in {0}'.format(post_directory))

    # Category selection
    while True:
        print('Select a category from the following list by its index')
        categories = list(posts_by_category())
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
    file_path = os.path.join(post_directory, f'{POST_FILENAME}.md')
    f = open(file_path, 'w')
    f.write('title: "{0}"\n'.format(title))
    f.write('date: {0}\n'.format(time.strftime('%Y-%m-%d')))
    f.write('category: {0}\n'.format(category))
    f.write('tags: [{0}]\n'.format(', '.join(tags)))
    f.write('feature: feature.png\n')
    f.write('description: ""\n')
    f.write('\n[TOC]\n')
    f.write('\n## Content\n')
    f.write("{% with video_id=\"XXXXXXXXXXX\" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}")
    f.close()
    print('\nCreated {0}'.format(file_path))

    # Create feature image file (no contents)
    feature_img = os.path.join(post_directory, 'feature.png')
    if not os.path.isfile(feature_img):
        f = open(feature_img, 'w')
        f.close()
        print('Created: {0}'.format(feature_img))


def serve_build():
    """ Server a build locally """
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
