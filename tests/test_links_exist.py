import re
import unittest

from bs4 import BeautifulSoup
import requests

from helpers import get_urls_from_html
from nitratine.__main__ import app


EXTERNAL_URL_BLACKLIST = [
    r'$^',
    r'^https://hitcounternitratine.pythonanywhere.com',  # Loves dying quite often at the moment
    r'^https://www.pexels.com',  # Keeps giving forbiddens?
    r'^https://nzcsc.org.nz'  # Doesn't seem to be up anymore
]
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'


class TestLinksRespondNon404(unittest.TestCase):
    def test_all_links_respond_non_404(self):
        test_client = app.test_client(self)
        local_links_visited = []
        local_links_to_visit = ['/']
        external_links_to_check = []

        # Initially only search local routes to build up a list of external links
        while len(local_links_to_visit) != 0:
            link = local_links_to_visit.pop()
            local_links_visited.append(link)

            response = test_client.get(link)
            self.assertEqual(response.status_code, 200, f'The path "{link}" returned HTTP{response.status_code}')

            # If a HTML response from this site was returned, look for other links on the page
            if 'text/html' in response.content_type:
                urls_within = get_urls_from_html(response.data.decode())
                local_links_to_visit += [
                    u for u in urls_within
                    if u.startswith('/')
                       and u not in local_links_visited
                       and u not in local_links_to_visit
                ]
                external_links_to_check += [
                    u for u in urls_within
                    if (not u.startswith('/')) and u not in external_links_to_check
                ]

        # Check all external links
        while len(external_links_to_check) != 0:
            link = external_links_to_check.pop()

            # Filter out some potential values we don't want
            if link.startswith('#') or link.startswith('mailto:') or link.startswith('javascript:'):
                continue

            # Validate external link is not in blacklist
            if any([re.match(r, link) is not None for r in EXTERNAL_URL_BLACKLIST]):
                continue

            # Request the URL and check it exists
            response = requests.get(
                link,
                verify=False,
                headers={'User-Agent': USER_AGENT}
            )
            self.assertEqual(response.status_code, 200, f'The path "{link}" returned HTTP{response.status_code}')

    def test_hash_references(self):
        test_client = app.test_client(self)
        pages = {}  # Store each page requested locally as a BeautifulSoup object
        links_visited = []
        links_to_visit = ['/']
        links_with_hashes_to_check = []

        # Initially only search local routes to build up a list of local links with hashes
        while len(links_to_visit) != 0:
            link = links_to_visit.pop()
            links_visited.append(link)

            # Get the page
            response = test_client.get(link)

            if 'text/html' in response.content_type:
                html = response.data.decode()
                pages[link] = BeautifulSoup(html, 'html.parser')  # Save as BeautifulSoup so we don't have to do this more than once per page
                urls_within = get_urls_from_html(html)
                links_to_visit += [
                    u for u in urls_within
                    if u.startswith('/')
                       and u.endswith('/')  # Do not look for hashes here
                       and u not in links_visited
                       and u not in links_to_visit
                ]
                # Links with hashes can either start with just a hash (for this page) or have a hash in them
                links_with_hashes_to_check += [link + u for u in urls_within if u.startswith('#')] \
                                + [u for u in urls_within if u.startswith('/') and '#' in u]  # Start with / for this site

        links_with_hashes_to_check = list(set(links_with_hashes_to_check))  # Distinct list
        while len(links_with_hashes_to_check) != 0:
            link = links_with_hashes_to_check.pop()
            self.assertEqual(1, link.count('#'), f'"{link}" has more than one "#"')
            # Identify the id and look for it on the page it is referencing
            route, id = link.split('#')
            soup = pages[route]
            self.assertNotEqual(None, soup.find(id=id))


if __name__ == '__main__':
    unittest.main()
