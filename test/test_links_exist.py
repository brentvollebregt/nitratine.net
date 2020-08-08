import re
from typing import List
import unittest

from bs4 import BeautifulSoup
import requests

from nitratine.__main__ import app


URL_CHECK_BLACKLIST = [
    r'^https://www.pexels.com',
    r'^https://nzcsc.org.nz',
    r'$^'
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
        # TODO Only search local pages first, then check all external with threading
        tester = app.test_client(self)
        links_visited = []
        links_to_visit = ['/']

        while len(links_to_visit) != 0:
            link = links_to_visit.pop()
            links_visited.append(link)

            if link.startswith('/'):
                response = tester.get(link)
                self.assertEqual(response.status_code, 200, link)

                # If a HTML response from this site was returned, look for other links on the page
                if 'text/html' in response.content_type:
                    urls_within = get_urls_from_html(response.data.decode())
                    links_to_visit += [
                        u for u in urls_within
                        if u not in links_visited
                           and u not in links_to_visit
                           and u not in URL_CHECK_BLACKLIST
                    ]
            elif link.startswith('#'):
                pass  # TODO Check hash is on page (different test)
            elif link.startswith('mailto:'):
                pass
            elif link.startswith('javascript:'):
                pass
            else:
                if any([re.match(r, link) is not None for r in URL_CHECK_BLACKLIST]):
                    continue

                response = requests.get(
                    link,
                    verify=False,
                    headers={'User-Agent': USER_AGENT}
                )
                self.assertEqual(response.status_code, 200, link)


if __name__ == '__main__':
    unittest.main()
