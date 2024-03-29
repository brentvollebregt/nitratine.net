title: "Hit Counter"
date: 2018-04-25
category: Projects
tags: [python, flask]
feature: feature.png
description: "Easily Count Hits on a Website by Requesting an SVG Displaying Hit Count. Works on any site."
github: brentvollebregt/hit-counter

<!-- <div style="text-align: center">
    <img src="https://hitcounter.pythonanywhere.com/nocount/tag.svg?url=https%3A%2F%2Fgithub.com%2Fbrentvollebregt%2Fhit-counter" alt="Hits">
</div> -->

~~Live demo hosted at: hitcounter.pythonanywhere.com~~

> PythonAnywhere has understandably disabled the demo instance due to heavy disk usage.

## What is This?
This is a server that allows a client to request an SVG file that displays views for a URL. This URL can either be passed as a query parameter or the referrer (or referer) value in the header will be used.

There is also a small method to prevent the refresh count increase issue (if you want to call it an issue, I see it as annoying) which uses cookies.

**This makes it very easy to keep track of views on static sites like Github Pages.** (can also be used on non-static sites as a general counter)

## How Can I Use it?
### Getting an SVG
To get an image for the current URL (for example is image is being requested by www.example.com), simply get the image as you normally would:

```html
<img src="https://hitcounter.pythonanywhere.com/count/tag.svg" alt="Hits">
```

In this example, a hit would be added to the websites count on the server. To stop this from occurring but still get the SVG file, use:

```html
<img src="https://hitcounter.pythonanywhere.com/nocount/tag.svg" alt="Hits">
```

### Getting the Count Raw
If you don't want the SVG file but still want the count to use in something else, you can do a GET request to ```/count``` or as before ```/nocount``` to not add a count. For Example:

```javascript
let xmlHttp = new XMLHttpRequest();
xmlHttp.open('GET', 'https://hitcounter.pythonanywhere.com/count', false);
xmlHttp.send(null);
count = xmlHttp.responseText;
```

### Getting a Count For a Site That Isn't Me
There may be circumstances that the referrer may not be sent or you may want to request an SVG or count for another site. To do this, add a query with ```url``` as the name and the URL you want to get (encoded obviously).

For example, getting an SVG:

```html
<img src="https://hitcounter.pythonanywhere.com/nocount/tag.svg?url=www.example.com" alt="Hits">
```

And if you want to get the count:

```javascript
let targetUrl = 'www.example.com';
let query = '?url=' + encodeURIComponent(targetUrl);
let xmlHttp = new XMLHttpRequest();
xmlHttp.open('GET', 'https://hitcounter.pythonanywhere.com/nocount' + query, false);
xmlHttp.send(null);
count = xmlHttp.responseText;
```

> There are also some situations where a client will not send the Referer in the header. This is a simple solution to the server not being able to find where the request came from.

## Generating Links With A Tool Hosted By The Server
Going to the location ```/``` on the server, you will be served with an HTML page that contains a tool to create the image tag or markdown element and search up a websites count.

![Interface](/posts/hit-counter/interface.png)

## Hosting Your Own Server
Running this server is very easy, simply clone the repo (or download the files) and run ```server.py```

I host this on pythonaywhere.com; to do this make sure you have cloned the repo into the filesystem and then create a new project. Modify the "WSGI configuration file" under the "Code" header in the "Web" tab. Change line 16 to import your script and restart the application using the green button at the top.

```python
from server import app as application
```

If you want to enable HTTPS on pythonaywhere, uncomment lines 5 and 8 in server.py to enable flask_sslify (is already installed on pythonaywhere, so you don't need to install it)

## How it Works
This server has been built with Flask. Calling one of the ```/count``` or ```/nocount``` methods will interact with the local SQLite3 database (file) and keep track of URLs, views and the counts for URLs. Data will be returned based on what is in the database at the current time.

Cookies are used to prevent multiple counts for the same client in a specified period. These are simply the URL as the key and a random string generated server-side as the value.

## Configuration
In config.py there are a few configurations that can be made
### DATABASE_FILENAME
This is the name of the SQLite3 database to be used, if it doesn't exist, it will be created. You don't need to worry about this unless you have conflicts with other applications.

### COOKIE_TIMEOUT
This is the amount of time for a client to count as a view again. When a view is counted, the SVG/count is returned with a cookie for that site. Currently, that is set at 1min (60 seconds) but can be changed.

To disable this feature simply set this to 0; the cookies stored on the server will be flushed from the database after each new view.

### SVG_TEMPLATE
This is the template of the SVG returned. ```{count}``` must always be in this string so that python can add the count before giving it as a response.

### RANDOM_VALUE_LENGTH
This is the length of the value of the cookie stored both server and client-side. Making this longer will stop collisions from occurring but will increase storage. Each value generated is completely random from the characters [0-9][a-z][A-Z].

## Inspiration
This project was inspired by [github.com/dwyl/hits](https://github.com/dwyl/hits) which is a "General purpose hits (page views) counter" which unfortunately will count GitHub repo views. This was my idea to expand on this and add some features with also making it compatible with any site.

## Why Does The Anti-Refresh System Not Work?
On sites like github.com, images are cached. Even though I declare no-cache in the header, GitHub will load the image on their side first which will cause an increase in the count no matter what as it isn't passing back the cookie it got previously (and if it did there would be a timeout for everyone).
