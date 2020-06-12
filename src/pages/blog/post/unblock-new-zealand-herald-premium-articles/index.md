---
templateKey: blog-post
title: "Unblock New Zealand Herald Premium Articles"
date: 2019-05-04T12:00:00.000Z
category: General
tags: [javascript, bookmarklet]
image: feature.png
description: 'A few days ago the site New Zealand Herald started to introduce premium content on their site. Using the JavaScript code in a bookmark found in this post is a very easy way to get around the monthly fee for "premium content".'
disableToc: false
hidden: true
---

## What is This?

A few days ago the site _New Zealand Herald_ started to introduce premium content on their site. This premium content contains articles that require you to pay a monthly fee to read. When looking at the source of the pages received, it's clear to see that full articles are still being sent to clients whether they are premium content or not.

I fully understand why they would do this; people now buy fewer papers so this is kind of like paying for the paper every week, just with this subscription you get a lot more. Unfortunately, the "paywall" that they have set up currently is a horrible attempt. I feel like they may be in a trial stage for the paywall's implementation which makes it very easy to get around.

This post contains JavaScript code (that runs on browsers) to help you easily remove the "mask" that hides premium article content.

> When going to any article on NZ Herald, you get sent the full article. CSS is then applied to specific elements with the `.paywall` class to hide the content. This script un-hides that content so you can see the full article.

## Latest Revision

This is the most recent version of the JavaScript bookmarklet. If you want to see the code, previous versions or a description of why this works, these will be found below.

<a class="btn btn-primary" href="javascript:copyCode()" role="button">Copy the Unblock Code</a>

<div class="alert alert-success" role="alert" id="copyCodeSuccess" style="display: none">
  JavaSript code has been copied!
</div>
<script type="text/javascript" src="/posts/unblock-new-zealand-herald-premium-articles/copy-to-clipboard.js"></script>

The button above copies the bookmarklet to your clipboard. Click this and then create a new bookmark (name it what you want) and paste the code copied into the bookmark address.

> On some devices you may find it easier to create a bookmark first with anything and then edit it to insert the code. Make sure the code copied starts with `javascript:` (it will if you copied it using the button).

### How to Use the Bookmarklet

When you're on an NZ Herald premium content page, simply open up your bookmarks and click on the bookmark you created. This will execute the code in the background and un-hide the post content.

> Websites Change: Please note that NZ Herald can change their site at any time, which means this could stop working at any time. If it has stopped working, feel free to comment below and I will look at what has changed.

## Revisions

This is a list of all the revisions of the script. If more information is discovered or the NZ Herald paywall system changes, a new revision will be made. You can copy the script from here if you wish, just make sure to add `javascript:` at the beginning when making it into a bookmark otherwise it will not execute.

### Original Script

The original script does three main things:

- Display any hidden content that is hidden by the `.paywall` class
- Hides the fade out of content before the subscription offer and the ellipsis' throughout some articles.
- Removes the subscription offer from the page

```javascript
(function () {
  $("#article-content.premium-content .paywall").css("display", "block");
  document.head.insertAdjacentHTML(
    "beforeEnd",
    "<style>#article-content.premium-content:before, #article-content.premium-content .ellipsis:after {content: none !important}</style>"
  );
  $(".article-offer").css("display", "none");
})();
```

### Revision 1

Looking in Reddit, I found a [post](https://www.reddit.com/r/newzealand/comments/bj9fdu/nz_herald_premium_content_for_free/) that had done the same task I had set out to do. Taking what I found here, I improved the original script and made it easier to read the source.

```javascript
(function () {
  $("head").append(
    "<style>" +
    "#main { height: auto !important }" +
    "#article-content.premium-content:before, #article-content.premium-content .ellipsis:after, .article-offer { display: none !important }" + // Paywall fix
      // '.pb-f-article-related-articles, .pb-f-global-recommend, .pb-f-global-blank-html { display: none !important }' + // General advertisement removal (I don't include it in the button but you can remove the recommended articles if you wish)
      "</style>"
  );
  $(".paywall").removeClass("paywall");
})();
```

### Revision 2 (7-5-19)

This one was a bit bigger because they are now making the CSS class that used to be `paywall` now a little bit more random. This can easily be solved by looking at all the classes in the content of the article and picking out the mode (not 100% accurate but does the job).

There is still a backup for any direct children of `#article-content` if this fails. Scrolling is turned back on, the offer is removed and some ads are removed.

```javascript
/* Throw some CSS in the head */
$("head").append(
  "<style>" +
  "#main { height: auto !important; }" /* Allow for scrolling */ +
  "#article-content > * { display: block !important; color: #000 !important; opacity: 1 !important; }" /* Show content (backup for class guess later) */ +
  ".article-offer { display: none !important; }" /* Remove 'offer' */ +
  ".ad-container, .pb-f-article-related-articles { display: none !important; }" /* Remove advertisements */ +
    "</style>"
);

/* A simple array mode function */
function mode(arr) {
  return arr
    .sort((a, b) => arr.filter(v => v === a).length - arr.filter(v => v === b).length)
    .pop();
}

let article_content = $("#article-content");

/* Get all the classes */
let classes = [];
article_content.children().each((index, e) => {
  e.classList.forEach(i => classes.push(i));
});

/* Try to find the mode of these classes and remove it (most likely the premium class) */
let possible_premium_class = mode(classes);
$("." + possible_premium_class).removeClass(possible_premium_class);

/* Remove the premium-content class. Removes fade out, ellipsis' */
article_content.removeClass("premium-content").addClass("full-content");
```

### Revision 3 (6-11-19)

It seems some sort of timer function has been implemented that checks for changes are redirects a user to a purchase page. Aside from this, `display: none` was also added inline to article elements which are no removed.

```javascript
/* Disable some tamper check? */
window.pwdf.a = function () {
  return false;
};

/* Throw some CSS in the head */
$("head").append(
  "<style>" +
  "#main { height: auto !important; } " /* Allow for scrolling */ +
  "#article-content { height: auto !important; overflow: auto !important; } " /* Show content in full height */ +
  "#article-content > * { display: block !important; color: #000 !important; opacity: 1 !important; } " /* Show content (backup for class guess later) */ +
  ".article-offer { display: none !important; } " /* Remove 'offer' */ +
  ".ad-container, .pb-f-article-related-articles { display: none !important; } " /* Remove advertisements */ +
    "</style>"
);

/* A simple array mode function */
function mode(arr) {
  return arr
    .sort((a, b) => arr.filter(v => v === a).length - arr.filter(v => v === b).length)
    .pop();
}

let article_content = $("#article-content");

/* Get all the classes */
let classes = [];
article_content.children().each((index, e) => {
  e.classList.forEach(i => classes.push(i));
});

/* Try to find the mode of these classes and remove it (most likely the premium class) */
let possible_premium_class = mode(classes);
$("." + possible_premium_class)
  .css("display", "")
  .removeClass(possible_premium_class);

/* Remove the premium-content class. Removes fade out, ellipsis' */
article_content.removeClass("premium-content").addClass("full-content");
```

### Revision 4 (18-12-19)

It seems `window.pwdf` is no longer used, I found a couple of solutions; going to use them both to potentially delay a new revision.

```javascript
/* Disable some tamper check? */
window.prtn = { f: btoa(window.env.HASH + window.location.href) };
isMobile.any = () => true;

/* Throw some CSS in the head */
$("head").append(
  "<style>" +
  "#main { height: auto !important; } " /* Allow for scrolling */ +
  "#article-content { height: auto !important; overflow: auto !important; } " /* Show content in full height */ +
  "#article-content > * { display: block !important; color: #000 !important; opacity: 1 !important; } " /* Show content (backup for class guess later) */ +
  ".article-offer { display: none !important; } " /* Remove 'offer' */ +
  ".ad-container, .pb-f-article-related-articles { display: none !important; } " /* Remove advertisements */ +
    "</style>"
);

/* A simple array mode function */
function mode(arr) {
  return arr
    .sort((a, b) => arr.filter(v => v === a).length - arr.filter(v => v === b).length)
    .pop();
}

let article_content = $("#article-content");

/* Get all the classes */
let classes = [];
article_content.children().each((index, e) => {
  e.classList.forEach(i => classes.push(i));
});

/* Try to find the mode of these classes and remove it (most likely the premium class) */
let possible_premium_class = mode(classes);
$("." + possible_premium_class)
  .css("display", "")
  .removeClass(possible_premium_class);

/* Remove the premium-content class. Removes fade out, ellipsis' */
article_content.removeClass("premium-content").addClass("full-content");
```

## Why Did I Write This?

People asked me to and I put it here for easy access. I don't even read the news.

### And That Shocking Artwork?

I am so sorry. Yes, I used MS Paint.

![Unblock New Zealand Herald Premium Articles Feature Image](feature.png)
