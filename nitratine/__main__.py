import argparse
import os
import socket

from .site import app, setup_minification
from .build import build
from .tools.new_post import new_post
from .tools.serve_build import serve_build
from .tools.build_stats import print_build_stats


def run():
    os.environ['build'] = 'Development'
    app.run(port=8000, host=socket.gethostbyname(socket.gethostname()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to run and build nitratine.net')
    parser.add_argument('-b', '--build', action="store_true", default=False, help='Build site to static files')
    parser.add_argument('-n', '--new-post', action="store_true", default=False, help='Create a new post')
    parser.add_argument('-s', '--serve-build', action="store_true", default=False, help='Serve the built site')
    parser.add_argument('--build-stats', action="store_true", default=False, help='Get stats for the latest build')
    parser.add_argument('--minify', action="store_true", default=False, help='Enable minification')
    args = parser.parse_args()

    if args.minify:
        setup_minification()

    if args.build:
        build()
    elif args.new_post:
        new_post()
    elif args.serve_build:
        serve_build()
    elif args.build_stats:
        print_build_stats()
    else:
        run()
