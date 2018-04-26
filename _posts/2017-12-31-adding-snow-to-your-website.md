---
layout: post
title: "Adding Snow to Your Website"
date: 2017-12-31
categories: Tutorials
tags: HTML CSS Website
---

* content
{:toc}

This is a quick and basic tutorial on how to add snow to your website. Files are provided and an example of this can be shown on the whole site.

<!-- more -->

## Adding the div
First you will need to add a div tag straight under the body tag. It can technically be placed anywhere, this is just recommended for location reasons. Give this div an id of "snow"

### Example
```html
<html>
    <head>
        Head content
    </head>
    <body>
        <div id="snow"></div>
        Body content
    </body>
</html>

```

## CSS
You will now need to add some CSS, whether it is in a style tag in the head or an external style sheet; it doesn't matter. A selector for the id snow and class snow need to be created. We will then create an animation using keyframes and images supplied below.

```css
#snow {
    pointer-events: none;
    position: fixed;
    height: 100%;
    width: 100%;
    left: 0;
    top: 0;
    z-index: 10;
}

.snow {
    background: url(/img/snow/s1.png), url(/img/snow/s2.png), url(/img/snow/s3.png);
    animation: snow 7s linear infinite;
}

@keyframes snow {
    0% { background-position: 0 0, 0 0, 0 0; }
    100% { background-position: 500px 1000px, 400px 400px, 300px 300px; }
}

```

### Images
Download the images below and save them (it looks like they are blank but they aren't)

[s1.png](/images/adding-snow-to-your-website/s1.png)
[s2.png](/images/adding-snow-to-your-website/s2.png)
[s3.png](/images/adding-snow-to-your-website/s3.png)

Depending on where you save these, you will need to change the background property vale in the snow class.

## Connecting CSS and Div
If you open your site now, nothing should have changed, apart from a div sitting there that can't be seen. You will need to add the snow class to the div tag to enable the snow. You can do this manually or if you want more control, you can attach some buttons to the following functions to turn the snow on and off.

```javascript
turnOnSnow = function () {
    var div = document.getElementById('snow');
    div.classList.add("snow");
};

turnOffSnow = function () {
    var div = document.getElementById('snow');
    div.classList.remove("snow");
};

```

By calling turnOnSnow() the snow will be enabled and to disable the snow call turnOffSnow()
