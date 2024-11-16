# [nitratine.net](https://nitratine.net/)

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fbrentvollebregt%2Fnitratine.net%2Fbadge&style=flat)](https://github.com/brentvollebregt/nitratine.net/actions?query=workflow%3A%22Build+and+Deploy+GitHub+Pages%22)

This repo is the source for [nitratine.net](https://nitratine.net/). The files in the `gh-pages` branch are hosted using GitHub pages. The Python module `nitratine` can be used to locally host and build the site into the `build` folder.

## Structure

```
📁 nitratine.net
┣ 📁 .github                 GitHub related files (like workflows)
┣ 📁 .vscode                 vs-code related settings
┣ 📁 nitratine               Main module that runs locally and freezes the site
┃ ┣ 📁 external              Functions that interact outside of the site
┃ ┣ 📁 markdown_extensions   Extensions for the markdown library used
┃ ┣ 📁 static                CSS, JavaScript and image files
┃ ┣ 📁 templates             Jinja templates for pages
┃ ┣ 📁 tools                 Tools that can be called from the modules CLI
┃ ┗ 📜 __main__.py           Module entrypoint to build and develop site
┣ 📁 posts                   Posts (markdown based)
┣ 📁 tests                   Tests associated with the module that runs the site locally
┗ 📜 .env.example            An example of the environment variables required
```

> This diagram contains a subset of all folders and files

## Setup

1. Create a virtual env: `python -m venv .venv`
2. Activate the Python venv: `.venv/Scripts/activate.bat`
3. Install Python dependencies: `python -m pip install -r requirements.txt`
4. Create a .env file: `cp .env.example .env`
5. Populate .env:
    - `YOUTUBE_DATA_API_KEY`: https://developers.google.com/youtube/v3/getting-started#before-you-start (get a simple token)

## Usage

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
