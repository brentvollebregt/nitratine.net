# brentvollebregt.pythonanywhere.com
Flask server running at brentvollebregt.pythonanywhere.com (in development)

This site is a simple blog that allows for pages to be added dynamically with added features

## Usage
Make sure you have Flask installed (pip install flask) and python (obviously).<br>
Run server.py to host the server; alternatively this can be imported and routes executed somewhere else (like pythonanywhere does).

## Articles
To add articles to the site...
Article layout
 - Root directory (specified in JSON (adding later))
    - sub (e.g. apps, blog, projects...)
        - Article name (what will be in the url)
            - data.json (Article info)
            - icon.png (Icon for article)
            - view.html (HTML page extending SKELETON.html)

data.json sample:
TODO

## Planning
- Home
    - Most viewed
    - Recent
    - Random Button
    - Small external links
- Projects
    - Top
    - Most recent
- Blog
    - Top
    - Most recent
- YouTube
    - Top
    - Most recent
- Tools
    - Most recently sorted
    - Squares with text backed by images
- Stats
    - # Of Articles
    - Page views

## Colours
 - Main: #1976d2
 - Light: #63a4ff
 - Dark: #004ba0
 - Main Highlight: #d81b60
 - Light Highlight: #ff5c8d
 - Dark Highlight: #a00037

## Stuff that needs to be stored
 - Article
    - ID
    - Sub location
    - Title
        - Small
        - Big
    - Desc
    - Tags
    - Views
        - Total
        - Last week (each indv day) ?
    - Content (img + text)
 - Views
    - Total
    - Hour contribution

Remember box shadows at the end

Media queries css

ICON - Blue writing with pink accents (+black and white) - transparent
