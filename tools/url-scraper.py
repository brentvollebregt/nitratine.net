"""
Identify URLs from HTML pages and search for further URLs under a given domain
"""

from bs4 import BeautifulSoup, SoupStrainer
from typing import List, Optional
import re

import requests


DOMAIN = 'nitratine.net'


def search_url(url: str) -> Optional[List[str]]:
    found_urls = []
    response = requests.get(url)

    if "text/html" not in response.headers['Content-Type']:
        # Not a HTML page
        print(f'\t[NOT HTML] {response.headers["Content-Type"]}')
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser', parse_only=SoupStrainer('a'))  # Only parse the a tags
        for link in soup:
            if link.has_attr('href'):
                href = link['href']

                if not (href.endswith('/') or re.search(r'\/#\w+$', href) is not None):
                    # Is not a HTML page (we assume)
                    continue

                if href.startswith('/'):
                    # Relative page
                    found_urls.append(f'https://{DOMAIN}{href}')
                elif href.startswith(f'https://{DOMAIN}') or href.startswith(f'http://{DOMAIN}'):
                     # Within the domain is the same as what we are looking for
                    found_urls.append(href)
    else:
        print(f'\t[HTTP{response.status_code}] {url}')

    return list(set(found_urls))  # Return a distinct list


urls = []
to_search = [f'https://{DOMAIN}/']

# Search URLs using breadth-first
while len(to_search) > 0:
    current_url = to_search.pop()  # Take out of the search list
    print(f'Searching: {current_url}')

    found_urls = search_url(current_url)  # Use this URL to search again
    if found_urls is not None:
        urls.append(current_url)  # Put into the found list
        to_search += [u for u in found_urls if u not in urls and u not in to_search]

# Print out all the URLs found
print('Search complete')
for u in urls:
    print(u)
