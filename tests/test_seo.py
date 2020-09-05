import re
import unittest

from bs4 import BeautifulSoup, SoupStrainer

from helpers import get_all_local_linked_pages
from nitratine.__main__ import app


IMAGE_ALT_EXCLUSIONS = [
    ['/about/', 'https://www.paypalobjects.com/en_US/i/scr/pixel.gif']
]


class TestSeo(unittest.TestCase):
    def test_all_pages_have_basic_seo(self):
        test_client = app.test_client(self)

        for link, response in get_all_local_linked_pages(test_client, '/'):
            if 'text/html' in response.content_type:
                soup = BeautifulSoup(response.data.decode(), 'html.parser')

                title = soup.find('title')
                description = soup.find('meta', attrs={"name": "description"})
                canonical = soup.find('link', attrs={"rel": "canonical"})

                self.assertNotEqual(None, title)
                self.assertNotEqual('', title.text)
                self.assertNotEqual(None, description)
                self.assertNotEqual('', description.get('content'))
                self.assertNotEqual(None, canonical)
                self.assertNotEqual('', canonical.get('href'))
            else:
                response.close()  # Stop warnings of the stream not being closed

    def test_all_images_have_alt_tags(self):
        test_client = app.test_client(self)

        for link, response in get_all_local_linked_pages(test_client, '/'):
            if 'text/html' in response.content_type:
                soup = BeautifulSoup(response.data.decode(), 'html.parser', parse_only=SoupStrainer('img'))
                for image in soup:
                    src = image.get('src')
                    alt = image.get('alt')

                    if any(e[0] == link and e[1] == src for e in IMAGE_ALT_EXCLUSIONS):
                        continue

                    self.assertNotEqual(None, alt, f'Image with src="{src}" on {link} has alt="{alt}"')
                    self.assertNotEqual('', alt, f'Image with src="{src}" on {link} has alt="{alt}"')
            else:
                response.close()  # Stop warnings of the stream not being closed

    def test_all_pages_have_reasonable_header_structures(self):
        test_client = app.test_client(self)

        for link, response in get_all_local_linked_pages(test_client, '/'):
            if 'text/html' in response.content_type:
                soup = BeautifulSoup(response.data.decode(), 'html.parser')
                headers = list(soup.find_all(re.compile('^h[1-6]$')))
                header_numbers = [int(i.name.replace('h', '')) for i in headers]
                if len(header_numbers) > 0:
                    max_header = max(header_numbers)
                    expected_headers = list(range(max_header, 0, -1))
                    for expected_header in expected_headers:
                        self.assertIn(expected_header, header_numbers, f'A h{max_header} exists but not a h{expected_header} on "{link}"')
                else:
                    self.fail(f'No headers found on "{link}"')
            else:
                response.close()  # Stop warnings of the stream not being closed


if __name__ == '__main__':
    unittest.main()
