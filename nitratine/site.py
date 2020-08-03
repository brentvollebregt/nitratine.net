import os
import time

from flask import Flask, render_template, send_from_directory, abort, render_template_string, url_for, redirect
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.toc import TocExtension

from .config import config, POST_SOURCE, POST_FILENAME, POST_EXTENSION, ASSETS_LOCATION
from .external.github import github_user_repos
from .external.youtube import recent_youtube_videos
from .flask_flatpages_extension import FlatPagesExtended


def my_renderer(text):
    pre_rendered_body = render_template_string(text)
    return markdown.markdown(
        pre_rendered_body,
        extensions=[
            CodeHiliteExtension(),
            ExtraExtension(),
            TocExtension()
        ]
    )


app = Flask(__name__)
app.config['FLATPAGES_AUTO_RELOAD'] = True
app.config['FLATPAGES_EXTENSION'] = POST_EXTENSION
app.config['FLATPAGES_ROOT'] = POST_SOURCE
app.config['FLATPAGES_HTML_RENDERER'] = my_renderer
posts = FlatPagesExtended(app, POST_FILENAME)


@app.route('/')
def index():
    """ The home page """
    for tile in config.home_tiles:  # TODO Mutability fix
        if tile['type'] == 'post':
            page = posts.get(tile['post'] + f'/{POST_FILENAME}')
            tile['link'] = url_for('blog_post', path=tile['post'])
            tile['title'] = page.meta.get('title', 'INVALID')
            tile['text'] = page.meta.get('description', 'INVALID')
            tile['date'] = ymd_format(page.meta.get('date', 'INVALID'))
            tile['image_url'] = url_for('post_assets', path=f'{tile["post"]}/{page.meta.get("feature", "INVALID")}')
        elif tile['type'] == 'post-image':
            tile['link'] = url_for('blog_post', path=tile['post'])

    return render_template(
        'home.html',
        tiles=config.home_tiles
    )


@app.route('/about/')
def about():
    """ The about page """
    build_time = time.strftime('%d/%m/%Y %H:%M:%S')
    return render_template('about.html', build_time=build_time)


@app.route('/portfolio/')
def portfolio():
    """ The portfolio page """
    return render_template('portfolio.html')


@app.route('/data/')
def data():
    """ The data page """
    public_posts = posts.get_posts()
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
        site_content=[{'meta': post.meta, 'path': post.path} for post in posts.get_posts()]
    )


@app.route('/blog/')
def blog_home():
    """ Page 1 of the blog feed """
    page1_posts = posts.paginate_posts(1)
    return render_template(
        'blog-home.html',
        category_numbers=posts.post_numbers_by_category(),
        pagination_nav=posts.get_pagination_nav_data(1),
        posts=page1_posts
    )


@app.route('/blog/page/<int:page>/')
def blog_pagination(page):
    """ Page n of the blog feed (or 404 if the page does not exist) """
    if page == 1:
        return redirect(url_for('blog_home'))
    if page < 1:
        abort(404)
    pagen_posts = posts.paginate_posts(page)
    if not pagen_posts:
        abort(404)
    return render_template(
        'blog-home.html',
        category_numbers=posts.post_numbers_by_category(),
        pagination_nav=posts.get_pagination_nav_data(page),
        posts=pagen_posts
    )


@app.route('/blog/categories/')
def blog_categories():
    """ Posts grouped by categories """
    return render_template(
        'blog-categories.html',
        category_numbers=posts.post_numbers_by_category(),
        categories=posts.posts_by_category(),
        title='Categories',
        sort_type='category'
    )


@app.route('/blog/tags/')
def blog_tags():
    """ Posts grouped by tags """
    return render_template(
        'blog-categories.html',
        category_numbers=posts.post_numbers_by_category(),
        categories=posts.posts_by_tag(),
        title='Tags',
        sort_type='tag'
    )


@app.route('/blog/archive/')
def blog_archive():
    """ Posts grouped and sorted by date """
    return render_template(
        'blog-categories.html',
        category_numbers=posts.post_numbers_by_category(),
        categories=posts.posts_by_date(),
        title='Date',
        sort_type='date'
    )


@app.route('/blog/post/<path:path>/')
def blog_post(path):
    """ A post. Renders the .md file. """
    post = posts.get_or_404(f'{path}/{POST_FILENAME}')

    github_repo = None
    if 'github' in post.meta:
        try:
            github_repo = [r for r in github_user_repos if r.full_name == post.meta.get('github')][0]
        except IndexError as e:
            print(f'The repository {post.meta.get("github")} was not found in github_user_repos')
            raise e

    return render_template(
        'blog-post.html',
        category_numbers=posts.post_numbers_by_category(),
        prev_and_next=posts.get_previous_and_next_posts(post),
        page=post,
        github_repo=github_repo
    )


# Site Management Routes


@app.route('/sitemap.xml')
def sitemap():
    """ The XML sitemap """
    pages = []
    for post in posts.get_posts():
        file_location = os.path.join(POST_SOURCE, post.path, f'{POST_FILENAME}{POST_EXTENSION}')
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


@app.route('/assets/<path:path>')  # TODO Make this use Flasks 'static' directory
def assets(path):
    """ Calls for files in the asset location """
    return send_from_directory(ASSETS_LOCATION, path)


@app.route('/posts/<path:path>')  # TODO Can we make this /post/ and make everything in the markdown files relative?
def post_assets(path):
    """ Calls for post assets. Technically this could return the post .md file but this has been disabled. """
    if path.endswith(f'/{POST_FILENAME}{POST_EXTENSION}'):
        abort(403)  # This file is not meant to be accessible from this route
    return send_from_directory(POST_SOURCE, path)


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
