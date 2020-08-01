import math
import time
from collections import defaultdict

import flask_flatpages

from .config import PAGINATION_PAGE_MAX, PAGINATION_EITHER_SIDE
from .utils import chunk_list


class FlatPagesExtended(flask_flatpages.FlatPages):
    def __init__(self, app, post_filename):
        """
        :param app: The Flask app to pass to flask_flatpages.FlatPages
        :param post_filename: The name of markdown files
        """
        super().__init__(app)
        self.post_filename = post_filename

    def get_posts(self, hidden=False, force_post=None):
        """ Get all posts in order of date.
        :param hidden: Whether to return hidden posts or not
        :param force_post: Whether to return a particular post no matter what
            (is used so hidden posts can see themselves in prev/next calculations)
        :return: Available posts
        """
        all_posts = [p for p in self if hidden or 'hidden' not in p.meta or force_post == p.path]
        all_posts.sort(key=lambda x: x.meta['date'], reverse=True)
        for post in all_posts:
            post.path = post.path.replace(f'/{self.post_filename}', '')
        return all_posts

    def posts_by_category(self):
        """ Get posts by category
        :return: {category: [post, post, ...]}
        """
        categories = defaultdict(list)
        for post in self.get_posts():
            category = post.meta.get('category', 'General')
            categories[category].append(post)
        return {t: categories[t] for t in sorted(categories)}

    def posts_by_tag(self):
        """ Get posts by tag
        :return: {tag: [post, post, ...]}
        """
        tags = defaultdict(list)
        for post in self.get_posts():
            post_tags = post.meta.get('tags', [])
            for tag in post_tags:
                tags[tag].append(post)
        posts_by_tag_unsorted = {t: tags[t] for t in sorted(tags)}
        return dict(sorted(posts_by_tag_unsorted.items()))

    def posts_by_date(self):
        """ Get posts by year
        :return: {year: [post, post, ...]}
        """
        years = defaultdict(list)
        for post in self.get_posts():
            post_date = post.meta.get('date', '1970-01-01')
            struct_time = time.strptime(str(post_date), '%Y-%m-%d')
            year = str(struct_time.tm_year)
            years[year].append(post)
        return years

    def post_numbers_by_category(self):
        """ Get number of posts per category
        :return: {category: count}
        """
        categories = self.posts_by_category()
        return {c: len(categories[c]) for c in categories}

    def paginate_posts(self, page):
        """ Get posts for a particular page
        :param page: The page number (0-indexed)
        :return: A list of posts on this page
        """
        page = page - 1  # Adjust to start a 0
        chunked_posts = list(chunk_list(self.get_posts(), PAGINATION_PAGE_MAX))
        if page > len(chunked_posts) - 1:
            return []
        return chunked_posts[page]

    def available_pagination_pages(self):
        """ Get the available pages
        :return: A list of page numbers that are available
        """
        chunked_posts = list(chunk_list(self.get_posts(), PAGINATION_PAGE_MAX))
        return list(range(1, len(chunked_posts) + 1))

    def get_pagination_nav_data(self, page):
        """ Calculate pages to show in navigation
        :param page: The page to get navigation data for
        :return: An object to create the pagination buttons
        """
        available_pages = self.available_pagination_pages()

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

    def get_previous_and_next_posts(self, post):
        """ Get the next and previous post for a particular post
        :param post: The post to get the previous and next post for
        :return: The previous and next post (either could be None)
        """
        # So we don't call it over and over again
        all_posts = self.get_posts(force_post=post.path)

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
