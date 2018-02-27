[![Header Image](https://i.imgur.com/I1bP0JU.png)](http://nitratine.pythonanywhere.com)
Flask server running at nitratine.pythonanywhere.com

## What is this?
I wanted to make a simple site that hosted my projects, tutorials and tools.<br>
It needed to be easy to add articles and be fully dynamic.<br>
It has a dark and light theme and allows you to turn snow particles on.

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
- Right sidebar that appears on wide enough devices with:
    - YouTube subscribe button
    - 6 most recent videos
    - Github card of your profile
    - Optional: 300x250 ad

## Running the Site Locally
1. Install Python
2. Clone this repo and cd into it
3. Execute ```pip install -r requirements.txt```
3. Run server.py
4. Go to /admin
    - Set variables on this page and change options
    - Set username and password using "Raw JSON" if needed

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
<link rel="stylesheet" type="text/css" class="css_dark_theme" href="{{ url_for('static', filename='css/dark/article.css') }}">
<link rel="stylesheet" type="text/css" class="css_light_theme" href="{{ url_for('static', filename='css/syntax_highlighting.css') }}">
<link rel="stylesheet" type="text/css" class="css_dark_theme" href="{{ url_for('static', filename='css/dark/syntax_highlighting.css') }}">
<script async src="{{ url_for('static', filename='js/article.js') }}"></script>
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
None of this is actually needed to make a page but it is just a structure I have created. Along with the variables passed in the example, extra_header_info and relative_url are also passed; relative_url being /sub/article.

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

## Screenshots
![Home Screen](https://i.imgur.com/WGHWSqjl.png)
![Article](https://i.imgur.com/spgdKTll.png)<br>
![Mobile Home Screen](https://i.imgur.com/rtgvXTCl.png)
![Mobile Menu](https://i.imgur.com/KMityGll.png)
![Mobile Article](https://i.imgur.com/OdPrsYGl.png)

# Maybe Later
- Integrate Good Analytics? - Analytics Reporting API v4 : Proper stats