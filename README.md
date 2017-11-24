# brentvollebregt.pythonanywhere.com
Flask server running at brentvollebregt.pythonanywhere.com (in development)

This site is a simple blog that allows for pages to be added dynamically with added features

## Usage
Make sure you have Flask installed (pip install flask) and python (obviously).<br>
Run server.py to host the server; alternatively this can be imported and routes executed somewhere else (like pythonanywhere does).

## Articles
To add articles to the site you will need to have defined the articles location in the servers data.json. They then need to follow a format to be detected on startup.
 - Root directory (specified in JSON (adding later))
    - sub (e.g. apps, blog, projects...)
        - Article name (what will be in the url)
            - data.json (Article info)
            - icon.png (Icon for article)
            - view.html (HTML page extending SKELETON.html)

#### data.json sample:
```json
{
  "title" : "Colour - The completely pointless app",
  "title_reduced" : "Colour - Android App",
  "description" : "This app is based off the goal of obtaining all 16,777,216 colours by randomly generating colours when taping the screen.",
  "tags" : ["Android", "App", "Java", "Random"],
  "date" : "18 Nov 17"
}
```

#### Article Layout Example
- articles
    - apps
        - colour
            - data.json
            - icon.png
            - view.html
    - blog
        - how-to-make-a-flask-site
            - data.json
            - icon.png
            - view.html
    - projects
    - tools
        - rbg-hex-converter
            - data.json
            - icon.png
            - view.html
    - youtube

These articles will be found at www.yourdomain.com/sub/article. e.g. brentvollebregt.pythonanywhere.com/apps/colour

## TODO
- Accessing navbar on smaller screens
- Administration
    - Edit article
    - Edit article JSON
    - Export stats
    - Edit JSON
    - Download and Upload JSON
    - Re-scrape pages
    - Remove Article (details and files)
<!--<link rel="icon" sizes="32x32" href="{{ url_for('static', filename='favicon.ico') }}">-->


## Colours
 - Main: #1976d2
 - Light: #63a4ff
 - Dark: #004ba0
 - Main Highlight: #d81b60
 - Light Highlight: #ff5c8d
 - Dark Highlight: #a00037

# Notes
Media queries css

ICON - Blue writing with pink accents (+black and white) - transparent

Stuff smaller?
- title 23px
- desc 13px
- tags 14px
