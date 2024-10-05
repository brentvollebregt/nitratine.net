import re
import unittest
from urllib3.exceptions import InsecureRequestWarning
import warnings

from bs4 import BeautifulSoup
import requests

from helpers import get_urls_from_html
from nitratine.__main__ import app


EXTERNAL_URL_BLACKLIST = [
    r'^$',
    r'^http://127.0.0.1',
    r'^http://localhost',
    r'^https://hitcounternitratine.pythonanywhere.com',  # Loves dying quite often at the moment
    r'^https://www.pexels.com',  # Keeps giving forbiddens?
    r'^https://nzcsc.org.nz',  # Doesn't seem to be up anymore
    r'^https://genius.com',  # 403
    r'^https://www.namesilo.com',  # 403
    r'^https://www.buymeacoffee.com',  # 403
    r'^https://www.digitalcitizen.life',  # 403
    r'^https://www.dabeaz.com',  # SSL error
    r'^https://www.tablesgenerator.com',  # SSL error
    r'^https://www.pdfescape.com',  # SSL error
    r'^https://www.lfd.uci.edu',  # SSL error
    r'^https://www.reddit.com',  # 403
    r'^https://stackoverflow.com',  # 403
    r'^https://cs.stackexchange.com',  # 403
    r'^https://raspberrypi.stackexchange.com',  # 403
    r'^https://crypto.stackexchange.com',  # 403
    r'^https://www.opendronemap.org',  # 403
    r'^https://simpleicons.org',  # 403
    r'^https://sourceforge.net'  # 403
]
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'


class TestLinksRespondNon404(unittest.TestCase):
    def test_all_links_respond_non_404(self):
        """
        Get all hrefs from the page and check that they return successful codes
        """
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
            else:
                response.close()  # Stop warnings of the stream not being closed

        failed_links_and_http_codes = []

        warnings.simplefilter("ignore", category=InsecureRequestWarning)

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
            try:
                status_code = -1
                response = requests.get(
                    link,
                    verify=False if link.startswith('http://') else True,  # Don't check SSL on HTTP links,
                    headers={'User-Agent': USER_AGENT}
                )
                status_code = response.status_code
                self.assertEqual(status_code, 200, f'The path "{link}" returned HTTP{status_code}')
            except Exception as e:
                print(f'Failed to get {link}: {e}')
                failed_links_and_http_codes.append([link, status_code])

        if len(failed_links_and_http_codes) > 0:
            error_list = ''
            for link_and_http_code in failed_links_and_http_codes:
                error_list += f'\n{link_and_http_code[1]} {link_and_http_code[0]}'
            self.fail(f'Paths were found that could not be requested:' + error_list)

        warnings.resetwarnings()

    def test_hash_references(self):
        """
        Validate that all local hash references are valid - the id exists on the page
        """
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
            else:
                response.close()  # Stop warnings of the stream not being closed

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
