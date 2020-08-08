# [nitratine.net](https://nitratine.net/)

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fbrentvollebregt%2Fnitratine.net%2Fbadge&style=flat)](https://github.com/brentvollebregt/nitratine.net/actions?query=workflow%3A%22Build+and+Deploy+GitHub+Pages%22)

This repo is the source for [nitratine.net](https://nitratine.net/). The files in the `gh-pages` branch are hosted using GitHub pages. The Python module `nitratine` can be used to locally host and build the site into the `build` folder.

Execute `python -m nitratine --help` to identify the functions that this module can perform and their arguments:

- `run`: Run the development site locally
- `build`: Build site to static files
- `serve`: Serve the locally built site
- `new`: Create a new post. Will setup a folder containing a .md file and an empty feature image.
- `stats`: Get stats for the latest build

## Deployment
Automated deployment is done using GitHub actions. The workflow to build and deploy the site can be found in [main.yml](/.github/workflows/main.yml).

## Testing
Tests can be run by executing `python -m unittest discover -s tests` in the root of the project.
