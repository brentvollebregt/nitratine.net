---
layout: post
title: "Github Badges"
date: 2018-04-25
categories: Tutorials
tags: Website
description: "A small demonstration of using GitHub badges from shields.io and how to manipulate them. Basic badges are demonstrated that would be most used by people."
---

* content
{:toc}

After recently making my project [{%- link _posts/2018-04-25-hit-counter.md -%}]({{ site.baseurl }}{%- link _posts/2018-04-25-hit-counter.md -%}) public, I was about to make a part to create your own custom badges to the project until I discovered [shields.io](https://shields.io/).

shields.io can be [found on Github](https://github.com/badges/shields) which is a server built in JavaScript to host "Concise, consistent, and legible badges in SVG and raster format". A lot of repositories with README.md files contain badges these days as they provide useful and interesting information.

In this tutorial I will show you how to create your own and some dynamic ones hosted by shields.io.

## Creating Your Own Static Badges
Going to [shields.io/#your-badge](https://shields.io/#your-badge) you will be brought down the page to a tool that lets you create your own badges. This is quite helpful if you want to make a static badge that either relies on human input or just doesn't change.

![Create Your Own Badge](/images/github-badges/static.png)

Entering a value in ```subject``` will provide the text for the left, ```status``` the value for the right and ```color``` the colour of the right part of the badge.

For example if I wanted to create a badge that says "made with" and then "python" with a blue background, I would do:

```html
<img src="https://img.shields.io/badge/made%20with-python-blue.svg" alt="made with python">
```

Which will give you: <img src="https://img.shields.io/badge/made%20with-python-blue.svg" alt="made with python" style="margin-bottom: -5px; display: inline-block;">

You can also use hex colour codes instead of names, for example:

```html
<img src="https://img.shields.io/badge/this%20is-purple-503040.svg" alt="this is purple">
```

This will give: <img src="https://img.shields.io/badge/this%20is-purple-503040.svg" alt="this is purple" style="margin-bottom: -5px; display: inline-block;">

<!-- more -->

## Styles
Five different styles are also available to use. These are:
 - Plastic (?style=plastic) <img src="https://img.shields.io/badge/style-plastic-green.svg?longCache=true&style=plastic" alt="Plastic" style="margin-bottom: -5px; display: inline-block;">
 - Flat (?style=flat) <img src="https://img.shields.io/badge/style-flat-green.svg?longCache=true&style=flat" alt="Flat" style="margin-bottom: -5px; display: inline-block;">
 - Flat Square (?style=flat-square) <img src="https://img.shields.io/badge/style-flat--square-green.svg?longCache=true&style=flat-square" alt="Flat Square" style="margin-bottom: -5px; display: inline-block;">
 - For The Badge (?style=for-the-badge) <img src="https://img.shields.io/badge/style-for--the--badge-green.svg?longCache=true&style=for-the-badge" alt="For The Badge" style="margin-bottom: -8px">
 - Social (?style=social) <img src="https://img.shields.io/badge/style-social-green.svg?longCache=true&style=social" alt="Social" style="margin-bottom: -5px; display: inline-block;">

To apply these styles to a badge, simple add `?style=` to the end of the url and then add the style type as shown in the brackets above.

For example, using my badge from before:

```html
<img src="https://img.shields.io/badge/made%20with-python-blue.svg?style=flat-square" alt="made with python">
```

Will create: <img src="https://img.shields.io/badge/made%20with-python-blue.svg?style=flat-square" alt="made with python" style="margin-bottom: -5px; display: inline-block;">

## Dynamic Badges
When visiting [shields.io](https://shields.io/) you will be introduces with a huge site of dynamic badges that the project supports. Here are a few badges that I like or find useful.

Remember there are many more badges on shields.io than what is displayed here. This is just a teaser and small examples of what is to offer.

### Github

Current GitHub tag: <img src="https://img.shields.io/github/tag/expressjs/express.svg" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/tag/expressjs/express.svg`

GitHub issues: <img src="https://img.shields.io/github/issues/badges/shields.svg" alt="GitHub issues" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/issues/badges/shields.svg`

GitHub contributors: <img src="https://img.shields.io/github/contributors/cdnjs/cdnjs.svg" alt="GitHub contributors" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/contributors/cdnjs/cdnjs.svg`

License: <img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="License" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/license/mashape/apistatus.svg`

GitHub code size in bytes: <img src="https://img.shields.io/github/languages/code-size/badges/shields.svg" alt="GitHub code size in bytes" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/languages/code-size/badges/shields.svg`

GitHub top language: <img src="https://img.shields.io/github/languages/top/badges/shields.svg" alt="GitHub top language" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/languages/top/badges/shields.svg`

GitHub language count: <img src="https://img.shields.io/github/languages/count/badges/shields.svg" alt="GitHub language count" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/languages/count/badges/shields.svg`

### Social

GitHub forks: <img src="https://img.shields.io/github/forks/badges/shields.svg?style=social" alt="Forks" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/forks/badges/shields.svg?style=social`

GitHub stars: <img src="https://img.shields.io/github/stars/badges/shields.svg?style=social" alt="Stars" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/stars/badges/shields.svg?style=social`

GitHub watchers: <img src="https://img.shields.io/github/watchers/badges/shields.svg?style=social" alt="Watchers" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/watchers/badges/shields.svg?style=social`

GitHub followers: <img src="https://img.shields.io/github/followers/espadrine.svg?style=social" alt="Followers" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/github/followers/espadrine.svg?style=social`

Twitter URL: <img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social" alt="Twitter" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/twitter/url/http/shields.io.svg?style=social`

Twitter Follow: <img src="https://img.shields.io/twitter/follow/pytutorials.svg?style=social&label=Follow" alt="Twitter Follow" style="margin-bottom: -5px; display: inline-block;">

`https://img.shields.io/twitter/follow/espadrine.svg?style=social&label=Follow`

## Additional Options
shields.io has also provided some parameters we can pass to allow for some customisation. To add these to the badge, just put `...svg?parameter=value`. If you already have a parameter, you can chain them using `&`.

For example, from `.svg?style=flat-square` to `.svg?style=flat-square&label=Tag&colorA=ff69b4`

Make sure to encode the uri before requesting. This can be done with the `encodeURIComponent()` method in JavaScript. For example encodeURIComponent(' ') is '%20'.

**?label=healthinesses : Override the default left-hand-side text**

<img src="https://img.shields.io/github/tag/expressjs/express.svg" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">  will become  <img src="https://img.shields.io/github/tag/expressjs/express.svg?label=healthinesses" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">

**?logo=appveyor : Insert one of the [named logos](https://github.com/badges/shields/tree/gh-pages/logo)**

<img src="https://img.shields.io/github/tag/expressjs/express.svg" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">  will become  <img src="https://img.shields.io/github/tag/expressjs/express.svg?logo=appveyor" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">

**?logo=data:image/png;base64,… : Insert custom logo image (≥ 14px high)**

No example as the data for the png will be large.

**?logoWidth=40 : Set the horizontal space to give to the logo**

<img src="https://img.shields.io/github/tag/expressjs/express.svg" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">  will become  <img src="https://img.shields.io/github/tag/expressjs/express.svg?logoWidth=40" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">

**?link=http://left&link=http://right : Specify what clicking on the left/right of a badge should do**

No example as I use img to embed these images (You can use an <object> tag if you want to embed these).

**?colorA=abcdef : Set background of the left part (hex color only)**

<img src="https://img.shields.io/github/tag/expressjs/express.svg" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">  will become  <img src="https://img.shields.io/github/tag/expressjs/express.svg?colorA=abcdef" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">

**?colorB=fedcba : Set background of the right part (hex color only)**

<img src="https://img.shields.io/github/tag/expressjs/express.svg" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">  will become  <img src="https://img.shields.io/github/tag/expressjs/express.svg?colorB=fedcba" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">

**?maxAge=360 : Set the HTTP cache lifetime in secs**

<img src="https://img.shields.io/github/tag/expressjs/express.svg" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">  will become  <img src="https://img.shields.io/github/tag/expressjs/express.svg?maxAge=360" alt="Current GitHub tag" style="margin-bottom: -5px; display: inline-block;">