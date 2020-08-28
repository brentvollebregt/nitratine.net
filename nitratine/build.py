import os

from .config import site_config, redirects, FREEZE_DESTINATION
from .site import app, page_not_found
from .freezer import freezer


def build():
    """ Build the site and dump it in FREEZER_DESTINATION """
    print('Freezing')
    freezer.freeze()

    # Create redirects (because Frozen-Flask doesn't have an option)
    for r in redirects:
        file_path = os.path.join(FREEZE_DESTINATION, r)
        file = os.path.join(file_path, 'index.html')
        # Check where we are writing
        if os.path.exists(file):
            print(f'WARN: Overwriting {file_path}')
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        # Write redirect
        f = open(file, 'w')
        with app.app_context():
            f.write(page_not_found(None, path=r))
        f.close()
        print(f'Redirect: /{r} -> /{redirects[r]}')

    # Add CNAME
    f = open(os.path.join(FREEZE_DESTINATION, 'CNAME'), 'w')
    f.write(site_config.domain)
    f.close()
    print('CNAME')

    # Add 404 page
    f = open(os.path.join(FREEZE_DESTINATION, '404.html'), 'w')
    with app.test_request_context():
        f.write(page_not_found(None)[0])
    f.close()
    print('404.html')
