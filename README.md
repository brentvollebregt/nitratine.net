# Nitratine
Flask server running at nitratine.pythonanywhere.com

## What is this?
I wanted to make a simple site that hosted my projects, tutorials and tools.<br>
It needed to be easy to add articles and be fully dynamic.

## Screenshots

## Features
- Easily add articles though a file explorer or administration panel
- Views are recorded for all articles
- Site split into five categories (the main ones I wanted)
- Easily edit site settings anywhere
- Pages displayed by popularity and date

## Usage
1. Install Python
2. Install Flask (```pip install Flask```)
3. Run server.py to make sure data.json generates
4. Edit data.json
    - site_location: only needed for robots.txt
    - articles_location: location of articles
    - administration: username and password for logging in at /admin
    - extra_header_info: A place to stick things like google analytics and verification tokens
    - descriptions: Edit descriptions of the six major pages

### Articles
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
  "title" : "Colour",
  "description" : "This app is based off the goal of obtaining all 16,777,216 colours by randomly generating colours when taping the screen.",
  "date" : "18 Nov 17"
}
```

#### view.html sample:
```
{% extends "SKELETON.html" %}

{% block head %}
<title>{{ title }} | Nitratine</title>
<meta name="description" content="{{ description }}" />
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/article.css') }}">
{% endblock %}

{% block content %}
<div class="article_content">
    <h1>{{ title }}</h1>
    <a class="date">{{ date }}</a><a class="views">{{ views }}</a>
    <p>{{ description }}</p>
</div>
{% endblock %}
```
Here we can see that the two blocks are extended from SKELETON.html. The article CSS file is added and relevant data passed to the template has been used including date, views, description and title; these are pulled from data.json.

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

### Pushing JSON
In /admin, there is a "Push JSON" button. This will write the current data in memory to data.json. Useful if the server is about to be stopped so the data and be re-imported.

### Re-Scraping Pages
In /admin, there is a "Re-scrape Pages" button. This checks all data.json article files for new data and will add any new articles if found.

### Exporting Stats
In /admin, there is a "Export Stats" button. This buttons will download a .json file of the current sites statistics.

### Data Manipulation
In /admin, there is a "Download JSON" and "Upload JSON" button. This allows you to download JSON to the text box underneath, edit and re-upload it to the server.

### CWD
In /admin, there is a "CWD" button. This button simple alerts the current working directory for debugging purposes.

### Article Management
In /admin, under "Download Article" you can enter a sub and an article name to download the article as a .zip<br>
Under that is a "Delete Article" section. This allows you to delete an article by entering a sub and an article name.<br>
Under that is a "Upload Article" section. This allows you to upload a zip file of an article by adding a file and entering a sub and an article name. These files need to be in the zip immediately (top level).<br>
Be aware that when downloading an article, the files need to be moved up to re-upload.

These articles will be found at www.yourdomain.com/sub/article. e.g. nitratine.pythonanywhere.com/apps/colour
