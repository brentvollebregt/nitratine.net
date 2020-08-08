from typing import List
import unittest

from bs4 import BeautifulSoup
import requests

from nitratine.__main__ import app


def get_urls_from_html(html: str) -> List[str]:
    links = []
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.findAll('a'):
        if link.get('href') is not None:
            links.append(link.get('href'))

    return list(set(links))


class TestLinksRespondNon404(unittest.TestCase):
    def test_all_links_respond_non_404(self):
        tester = app.test_client(self)
        links_visited = []
        links_to_visit = ['/']

        while len(links_to_visit) != 0:
            link = links_to_visit.pop()
            links_visited.append(link)
            print(link)

            if link.startswith('/'):
                response = tester.get(link)
                self.assertEqual(response.status_code, 200, link)
                content_type = response.content_type

                # If a HTML response from this site was returned, look for other links on the page
                if 'text/html' in content_type and link.startswith('/'):
                    urls_within = get_urls_from_html(response.data.decode())
                    links_to_visit += [
                        u for u in urls_within
                        if u not in links_visited
                           and u not in links_to_visit
                    ]
            elif link.startswith('#'):
                pass  # TODO Check hash is on page (different test)
            elif link.startswith('mailto:'):
                pass
            else:
                response = requests.get(link, verify=False)
                self.assertEqual(response.status_code, 200, link)


if __name__ == '__main__':
    unittest.main()
