from datetime import datetime
import os
import time
import urllib.parse

from flask import Flask, render_template, send_from_directory, abort, url_for, redirect, request
from flask_minify import minify
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.toc import TocExtension

from .config import site_config, redirects, featured_posts, POST_SOURCE, POST_FILENAME, POST_EXTENSION
from .external.github import get_github_user_repos
from .external.youtube import get_most_recent_youtube_videos
from .flask_flatpages_extension import FlatPagesExtended
from .markdown_extensions import YouTubeVideoExtension, HeaderLinkExtension
from .rss import generate_rss_xml


active_markdown_extensions = [
    CodeHiliteExtension(),  # Code highlighting
    ExtraExtension(),
    TocExtension(),  # Table of contents `[toc]` + header ids
    YouTubeVideoExtension(),  # `youtube:<video_id>` tag
    HeaderLinkExtension()  # Adding chain hover icon to go to header hash link
]


app = Flask(__name__)
app.config['FLATPAGES_AUTO_RELOAD'] = True
app.config['FLATPAGES_EXTENSION'] = POST_EXTENSION
app.config['FLATPAGES_ROOT'] = POST_SOURCE
app.config['FLATPAGES_HTML_RENDERER'] = lambda md: markdown.markdown(md, extensions=active_markdown_extensions)
posts = FlatPagesExtended(app, POST_FILENAME)


def setup_minification():
    minify(app=app, caching_limit=0, bypass=[r'fuzzysort.js', r'^rss$'])


@app.route('/')
def index():
    """ The home page """
    translated_featured_posts = []
    for tile in featured_posts:
        translated_featured_post = {'type': tile.type}
        page = posts.get(tile.post + f'/{POST_FILENAME}')
        translated_featured_post['link'] = url_for('blog_post', path=tile.post)

        if tile.type == 'post':
            translated_featured_post['title'] = page.meta.get('title', 'INVALID')
            translated_featured_post['text'] = page.meta.get('description', 'INVALID')
            translated_featured_post['date'] = ymd_format(page.meta.get('date', 'INVALID'))
            translated_featured_post['image_url'] = url_for('post_assets', path=f'{tile.post}/{page.meta.get("feature", "INVALID")}')
            translated_featured_post['category'] = page.meta.get('category', 'INVALID')
        elif tile.type == 'post-image':
            translated_featured_post['image_url'] = url_for('post_assets', path=f'{tile.post}/{page.meta.get("feature", "INVALID")}')
        elif tile.type == 'raw':
            translated_featured_post['content'] = tile.content

        translated_featured_posts.append(translated_featured_post)

    return render_template(
        'page/home.html',
        tiles=translated_featured_posts
    )


@app.route('/about/')
def about():
    """ The about page """
    build_time = time.strftime('%d/%m/%Y %H:%M:%S')
    return render_template('page/about.html', build_time=build_time)


@app.route('/portfolio/')
def portfolio():
    """ The portfolio page """
    return render_template('page/portfolio.html')


@app.route('/data/')
def data():
    """ The data page """
    public_posts = posts.get_posts()
    available_posts = [[p.path, p['title']] for p in public_posts]

    return render_template(
        'page/data.html',
        repos=get_github_user_repos(),
        posts=available_posts
    )


@app.route('/search/')
def search():
    """ The search page """
    return render_template(
        'page/search.html',
        site_content=[{'meta': post.meta, 'path': post.path} for post in posts.get_posts()]
    )


@app.route('/blog/')
def blog_home():
    """ Page 1 of the blog feed """
    page1_posts = posts.paginate_posts(1)
    return render_template(
        'blog-home.html',
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
        pagination_nav=posts.get_pagination_nav_data(page),
        posts=pagen_posts
    )


@app.route('/blog/categories/')
def blog_categories():
    """ Posts grouped by categories """
    return render_template(
        'blog-categories.html',
        categories=posts.posts_by_category(),
        title='Categories',
        sort_type='category'
    )


@app.route('/blog/tags/')
def blog_tags():
    """ Posts grouped by tags """
    return render_template(
        'blog-categories.html',
        categories=posts.posts_by_tag(),
        title='Tags',
        sort_type='tag'
    )


@app.route('/blog/archive/')
def blog_archive():
    """ Posts grouped and sorted by date """
    return render_template(
        'blog-categories.html',
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
            github_repo = [r for r in get_github_user_repos() if r.full_name == post.meta.get('github')][0]
        except IndexError as e:
            print(f'The repository {post.meta.get("github")} was not found in github_user_repos')
            raise e

    return render_template(
        'blog-post.html',
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

    return render_template('sitemap.xml', pages=pages), 200, {'content-type': 'text/xml'}


@app.route('/rss.xml')
def rss():
    """ The RSS Feed """
    return generate_rss_xml(posts), 200, {'content-type': 'text/xml'}


@app.route('/ads.txt')
def ads_txt():
    """ An easy way to generate ads.txt """
    return f'google.com, {site_config.google_adsense_publisher_id}, DIRECT, f08c47fec0942fa0', 200, {'content-type': 'text/plain'}


@app.route('/posts/<path:path>')  # TODO Can we make this /post/ and make everything in the markdown files relative - rename folder to post?
def post_assets(path):
    """ Calls for post assets. Technically this could return the post .md file but this has been disabled. """
    if path.endswith(f'/{POST_FILENAME}{POST_EXTENSION}'):
        abort(403)  # This file is not meant to be accessible from this route
    return send_from_directory(POST_SOURCE, path)


@app.errorhandler(404)
def page_not_found(e, path=None):
    """ Catches any unhandled routes. Used to identify potential redirects otherwise serves a 404 page. """
    cut_down_path = request.path[1:-1] if path is None else path  # Lose front and back forward slashes: /path/to/here/ => path/to/here
    if cut_down_path in redirects:
        return render_template(
            'redirect.html',
            redirect_to=f'/{redirects[cut_down_path]}/'
        )
    return render_template('404.html'), 404


# Injectors


@app.context_processor
def inject_site():
    """ Provide site_config to Jinja templates """
    return dict(site_config=site_config)


@app.context_processor
def inject_recent_videos():
    """ Provide recent_videos to Jinja templates """
    return dict(recent_videos=get_most_recent_youtube_videos())


@app.context_processor
def inject_category_numbers():
    """ Provide category_numbers to Jinja templates (for sidebar in blog-base.html) """
    return dict(category_numbers=posts.post_numbers_by_category())


@app.context_processor
def inject_now():
    """ Provide the current date """
    return {'now': datetime.utcnow()}


def ymd_format(date):
    """ Convert 2018-10-30 to 30 Nov 2018 """
    struct_time = time.strptime(str(date), '%Y-%m-%d')
    return f'{struct_time.tm_mday} {time.strftime("%b", struct_time)} {struct_time.tm_year}'


def url_encode(string):
    """ Convert a string to be used in a query string """
    return urllib.parse.quote_plus(string)


app.jinja_env.globals.update(ymd_format=ymd_format)  # Allow ymd_format to be called in a Jinja template
app.jinja_env.globals.update(url_encode=url_encode)  # Allow ymd_format to be called in a Jinja template
