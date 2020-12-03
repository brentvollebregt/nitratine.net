from pathlib import Path

import click
from livereload import Server

from .site import app, setup_minification
from .build import build as build_site
from .tools.new_post import new_post
from .tools.serve_build import serve_build
from .tools.build_stats import print_build_stats
from .config import POST_SOURCE, site_config


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8000


@click.group()
def cli():
    """ Nitratine """


@cli.command()
@click.option('-h', '--host', 'host', default=DEFAULT_HOST, help="Hostname to run server with")
@click.option('-p', '--port', 'port', type=int, default=DEFAULT_PORT, help="Port to run server on")
@click.option('--minify', 'minify', is_flag=True, default=False, help="Enable minification")
@click.option('--watch', 'watch', is_flag=True, default=False, help="Enable live-reload and watch for changes")
@click.option('--prod', '--production', 'production', is_flag=True, default=False, help="Don't change the site URL")
def run(host: str, port: int, minify: bool, watch: bool, production: bool):
    """ Run the development site locally """
    if minify:
        setup_minification()

    if not production:
        site_config.url = f'http://{host}:{port}'

    if watch:
        server = Server(app)
        server.watch(POST_SOURCE)
        server.watch(str(Path(__file__).resolve().parent / 'static'))
        server.serve(host=host, port=port)
    else:
        print(f'Server starting at http://{host}:{port}')
        app.run(host=host, port=port)


@cli.command()
@click.option('--minify', 'minify', is_flag=True, default=False, help="Enable minification")
def build(minify: bool):
    """ Build site to static files """
    if minify:
        setup_minification()

    build_site()


@cli.command()
@click.option('-p', '--port', 'port', type=int, default=DEFAULT_PORT, help="Port to run server on")
def serve(port: int):
    """ Serve the locally built site """
    serve_build(port)


@cli.command()
def new():
    """ Create a new post """
    new_post()


@cli.command()
def stats():
    """ Get stats for the latest build """
    print_build_stats()


if __name__ == '__main__':
    cli(prog_name='nitratine')
