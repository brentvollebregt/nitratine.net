import re
import unittest

from bs4 import BeautifulSoup

from helpers import get_all_local_linked_pages
from nitratine.__main__ import app


class TestCoverage(unittest.TestCase):
    def test_codehillite_class_coverage(self):
        test_client = app.test_client(self)

        # Get all currently defined CSS classes relating to codehilite
        pygments_css_file = test_client.get('/static/css/pygments.css')
        pygments_css = pygments_css_file.data.decode()
        defined_classes = re.compile('\.codehilite \.([a-z0-9]+) {', re.MULTILINE).findall(pygments_css)

        # Identify all existing classes on site and check they are defined
        for link, response in get_all_local_linked_pages(test_client, '/'):
            if 'text/html' in response.content_type:
                soup = BeautifulSoup(response.data.decode(), 'html.parser')
                code_elements = soup.select('div.codehilite > pre span')
                for element in code_elements:
                    if 'class' in element.attrs:
                        for _class in element.attrs['class']:
                            self.assertIn(_class, defined_classes, f'Class {_class} not defined (from {link})')


if __name__ == '__main__':
    unittest.main()
