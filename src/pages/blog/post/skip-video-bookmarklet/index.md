---
templateKey: blog-post
title: "Skip Video Bookmarklet"
date: 2018-12-03T00:00:00.000+12:00
category: General
tags: [javascript]
feature:
description: "This bookmarklet allows you to skip videos that are playing on the current site. This means it can be used to skip forced videos like YouTube ads. Not all video players are supported."
disableToc: false
hidden: true
---

## What is a Bookmarket?

A [bookmarlet](https://en.wikipedia.org/wiki/Bookmarklet) is a bookmark that runs JavaScript code. This allows someone to easily create something like a button that will execute JavaScript when clicked.

## Adding the Bookmarket

To add the bookmarket, simply click and drag the link below into your bookmark bar.

<a href="javascript:videos = document.getElementsByTagName('video'); for (i = 0; i < videos.length; i++) { videos[i].currentTime = videos[i].duration; }">Skip Video</a>

If you cannot drag this onto the bookmark bar, right-click on it and copy the link address. Next, create a new bookmark and add this as the URL.

## The Code

You don't need to copy this code (_instructions above_); this is simply for curiosity.

```javascript
videos = document.getElementsByTagName("video");
for (i = 0; i < videos.length; i++) {
  videos[i].currentTime = videos[i].duration;
}
```

To make this a bookmarklet, you will need to create a new bookmark, add `javascript:` and then paste the JavaScript code in.
