# [nitratine.net](https://nitratine.net/)
This repo is the source for nitratine.net. The files in the `docs\` folder are hosted using GitHub pages. `site.py` can be used to locally host and build the site into the docs folder.

`site.py` takes arguments to do different functions:
 - No arguments: Locally host the site on port 8000. 
 - `-b` / `--build`: Build the site in the docs folder.
 - `-s` / `--serve-build`: Server the build site in the docs folder on port 8000.
 - `-n` / `--new-post`: Create a new post. Will create the .md file with a small template and create a folder for assets as well as copy in the default feature image.

### TODO
 - Fix site font sizes 
    - body {font-size: 0.94rem;}
    - h1 {font-size: 2rem;}
 - Compress images where they can be (https://imagecompressor.com/)
 - Internally: 
