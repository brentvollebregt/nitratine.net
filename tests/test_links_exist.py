import re
from typing import List
import unittest

from bs4 import BeautifulSoup
import requests

from nitratine.__main__ import app


EXTERNAL_URL_BLACKLIST = [
    r'$^',
    r'^https://www.pexels.com',
    r'^https://nzcsc.org.nz'
]
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'


def get_urls_from_html(html: str) -> List[str]:
    links = []
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.findAll('a'):
        if link.get('href') is not None:
            links.append(link.get('href'))

    return list(set(links))


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
                continue  # TODO Check hash is on page (different test)

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


if __name__ == '__main__':
    unittest.main()
