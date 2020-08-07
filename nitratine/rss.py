import datetime

from feedgen.feed import FeedGenerator
from flask import url_for

from .config import config
from .utils import get_nzst_timezone_for_date


def generate_rss_xml(posts):
    """ Generate an RSS feed as XML """
    fg = FeedGenerator()
    fg.id(config.site.domain)
    fg.title(config.site.title)
    fg.author({'name': config.site.default_author, 'email': config.site.email})
    fg.link(href=config.site.url, rel='alternate')
    fg.logo(f'{config.site.url}/static/img/favicon.ico')
    fg.subtitle('A place where I share projects developed by me and tutorials on topics that I\'m interested in.')  # TODO Make a constant also
    fg.language('en')

    for post in posts.get_posts():
        path = f'{config.site.url}{url_for("blog_post", path=post.path)}'
        title = post.meta.get('title')
        date = post.meta.get('date')
        category = post.meta.get('category')
        description = post.meta.get('description')
        feature_image_path = f'{config.site.url}/posts/{post.path}/{post.meta.get("feature")}'

        fe = fg.add_entry()
        fe.id(path)
        fe.title(title)
        fe.link(href=path)
        fe.category({'term': category, 'label': category})
        fe.published(datetime.datetime.combine(date, datetime.time(0, 0, tzinfo=get_nzst_timezone_for_date(date))))
        fe.description(description)
        fe.enclosure(feature_image_path, length=0, type=f'image/{feature_image_path.split(".")[-1]}')
        fe.content(post.html, type='text/html')

    return fg.rss_str(pretty=True)
