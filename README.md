# [nitratine.net](https://nitratine.net/)

![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fbrentvollebregt%2Fnitratine.net%2Fbadge&style=flat)

This repo is the source for nitratine.net. The files in the `gh-pages` branch are hosted using GitHub pages. `site.py` can be used to locally host and build the site into the `build` folder.

`site.py` takes arguments to do different functions:
 - No arguments: Locally host the site on port 8000. 
 - `-b` / `--build`: Build the site into the `build` folder.
 - `-s` / `--serve-build`: Server the build site in the `build` folder on port 8000.
 - `-n` / `--new-post`: Create a new post. Will create the .md file with a small template and create a folder for assets as well as copy in the default feature image.
 
## Deployment
Automated deployment is done using GitHub actions. The workflow to build and deploy the site can be found in [main.yml](/.github/workflows/main.yml).
