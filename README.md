[![Header Image](https://i.imgur.com/I1bP0JU.png)](http://nitratine.pythonanywhere.com)
Flask server running at nitratine.pythonanywhere.com

## What is this?
I wanted to make a simple site that hosted my projects, tutorials and tools.<br>
It needed to be easy to add articles and be fully dynamic.<br>
It has a dark and light theme and allows you to turn snow particles on.

## Screenshots
![Home Screen](https://i.imgur.com/WGHWSqjl.png)
![Article](https://i.imgur.com/spgdKTll.png)<br>
![Mobile Home Screen](https://i.imgur.com/rtgvXTCl.png)
![Mobile Menu](https://i.imgur.com/KMityGll.png)
![Mobile Article](https://i.imgur.com/OdPrsYGl.png)

## Features
- Easily add articles though a file explorer or administration panel
- Views are recorded for all articles
- Site split into five categories (the main ones I wanted)
- Easily edit site settings anywhere
- Pages displayed by popularity and date
- Switch between light and dark themes
- Option to switch snow on
- Supports smaller screen sizes
- Has a different menu for smaller devices
- Run python code server side

## Usage
1. Install Python
2. Install Flask (```pip install Flask```)
3. Run server.py to make sure data.json generates
4. Edit data.json
    - site_location: only needed for robots.txt (e.g. "http://nitratine.pythonanywhere.com")
    - administration: username and password for logging in at /admin
    - extra_header_info: A place to stick things like google analytics and verification tokens
    - descriptions: Edit descriptions of the six major pages (descriptions for articles can be defined in the article itself or use the "description" variable passed to the Jinja template.

### Articles
Articles will be searched for in articles/ which will be in the same directory as server.py. They then need to follow a format to be detected on startup.
 - articles/
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

### Server Side Scripting
By putting python files in an articles folder, a script can be called at the path /scripts/[sub]/[article]/[script]. The Python file needs to contain a main method that takes the request as a parameter. The main method must return something to be passed back to the client.
```python
def main(request):
    """Do Stuff"""
    return {"success" : True}
```
The object returned from the main method is what will be returned to the client. This means if you want to return a JSON object, it would be recommended to jsonify it first.

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

### Redirects
Redirects can currently only be modified in the raw JSON. To set up a redirect, go to "redirects" in the json and create a new key-value pair in the dictionary. They key is the request.path (e.g. /to/be/redirected) and the value is where to redirect to (e.g./redirect/to/here). For example:
```json
"redirects" : {
    "/apps/color": "/apps/colour",
    "/colour" : "/apps/colour"
}
```

### Push Per View
Push per view saves the data in memory to data.json whenever a view is added. This saves you from having to push the data before each restart of the server (can lose data if you forget to push). Set to true to enable.

# TODO
- Ignore IP list
- Add more stuff to admin
    - Easily set redirects
    - Set site location with one click
    - Add me for ignore ip list
    - Articles location
    - Edit descriptions
    - Admin sub selection drop down
- Dynamically able to add subs? (might not be worth it)