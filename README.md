# [nitratine.net](https://nitratine.net/)
This repo is the source for nitratine.net. The files in the `gh-pages` branch are hosted using GitHub pages. `site.py` can be used to locally host and build the site into the docs folder.

`site.py` takes arguments to do different functions:
 - No arguments: Locally host the site on port 8000. 
 - `-b` / `--build`: Build the site into the docs folder.
 - `-s` / `--serve-build`: Server the build site in the docs folder on port 8000.
 - `-n` / `--new-post`: Create a new post. Will create the .md file with a small template and create a folder for assets as well as copy in the default feature image.
 
## Deployment
An automated deployment system can be found in `deploy.py` which when run, will build the site, clone `gh-pages` branch from GitHub, swap out the build, commit, tag and push. 
