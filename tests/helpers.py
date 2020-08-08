from typing import List

from bs4 import BeautifulSoup


def strip_hash(url):
    if '#' in url:
        return ''.join(url.split('#')[:-1])
    return url


def get_urls_from_html(html: str) -> List[str]:
    """ Identify all the links from HTML """
    links = []
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.findAll('a'):
        if link.get('href') is not None:
            links.append(link.get('href'))

    # TODO Add script sources

    return list(set(links))


def get_all_local_linked_pages(test_client, start_route):
    local_links_visited = []
    local_links_to_visit = [start_route]

    # Initially only search local routes to build up a list of external links
    while len(local_links_to_visit) != 0:
        link = local_links_to_visit.pop()
        local_links_visited.append(link)

        response = test_client.get(link)

        if 'text/html' in response.content_type:
            urls_within = get_urls_from_html(response.data.decode())
            urls_within_with_no_hashes = map(strip_hash, urls_within)
            local_links_to_visit += [
                u for u in urls_within_with_no_hashes
                if u.startswith('/')
                   and u not in local_links_visited
                   and u not in local_links_to_visit
            ]

        yield link, response
