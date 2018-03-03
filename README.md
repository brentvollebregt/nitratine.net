[![Header Image](https://i.imgur.com/I1bP0JU.png)](http://nitratine.pythonanywhere.com)
Flask server running at nitratine.pythonanywhere.com

## What is this?
I wanted to make a simple site that hosted my projects, tutorials and tools.<br>
It needed to be easy to add articles and be fully dynamic.<br>
It has a dark and light theme and allows you to turn snow particles on.

<details>
  <summary>Features</summary>
  <ul>
    <li>Easily add articles though a file explorer or administration panel</li>
    <li>Views are recorded for all articles</li>
    <li>Site split into five categories (the main ones I wanted)
    <li>Easily edit site settings anywhere
    <li>Pages displayed by popularity and date
    <li>Switch between light and dark themes
    <li>Option to switch snow on
    <li>Supports smaller screen sizes
    <li>Has a different menu for smaller devices
    <li>Run python code server side
    <li>Right sidebar that appears on wide enough devices with:
        <ul>
            <li>YouTube subscribe button</li>
            <li>6 most recent videos</li>
            <li>Github card of your profile</li>
            <li>Optional: 300x250 ad</li>
        </ul>
    </li>
  </ul>
</details>

## Running the Site Locally
1. Install Python
2. Clone this repo and cd into it
3. Execute ```pip install -r requirements.txt```
3. Run server.py
4. Go to /admin
    - Set variables on this page and change options
    - Set username and password using "Raw JSON" if needed

### Format and Layout Articles
Articles will be searched for in articles/ which will be in the same directory as server.py. They then need to follow a format to be detected on startup.
 - articles/
    - sub (e.g. apps, blog, projects...)
        - Article name (what will be in the url)
            - data.json (Article info)
            - icon.png (Icon for article)
            - view.html (HTML page extending SKELETON.html)

<details>
  <summary>Article Folder Layout Example</summary>
    <li>articles
        <ul>
            <li>apps
                <ul>
                    <li>colour
                        <ul>
                            <li>data.json</li>
                            <li>icon.png</li>
                            <li>view.html</li>
                        </ul>
                    </li>
                </ul>
        </li>
            <li>blog
                <ul>
                    <li>colour
                        <ul>
                            <li>data.json</li>
                            <li>icon.png</li>
                            <li>view.html</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li>projects</li>
            <li>tools
                <ul>
                    <li>colour
                        <ul>
                            <li>data.json</li>
                            <li>icon.png</li>
                            <li>view.html</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li>youtube</li>
        </ul>
    </li>
</details>

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

### Server Side Scripting
By putting python files in an articles folder, a script can be called at the path /scripts/[sub]/[article]/[script].py. The Python file needs to contain a main method that takes the request as a parameter. The main method must return something to be passed back to the client.
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