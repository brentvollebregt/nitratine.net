title: "Unblock New Zealand Herald Premium Articles"
date: 2019-05-04
category: General
tags: [javascript, bookmarklet]
feature: feature.png
description: "A few days ago the site New Zealand Herald started to introduce premium content on their site. Using the JavaScript code in a bookmark found in this post is a very easy way to get around the monthly fee for \"premium content\"."
hidden: true

[TOC]

## What is This?
A few days ago the site *New Zealand Herald* started to introduce premium content on their site. This premium content contains articles that require you to pay a monthly fee to read. When looking at the source of the pages received, it's clear to see that full articles are still being sent to clients whether they are premium content or not.

I fully understand why they would do this; people now buy less papers so this is kind of like paying for the paper every week, just with this subscription you get a lot more. Unfortunately the "paywall" that they have set up currently is a horrible attempt. I feel like they may be in a trial stage for the paywall's implementation which makes it very easy to get around.

This post contains JavaScript code (that runs on browsers) to help you easily remove the "mask" that hides premium article content.

> When going to any article on NZ Herald, you get sent the full article. CSS is then applied to specific elements with the `.paywall` class to hide the content. This script un-hides that content so you can see the full article.

## Latest Revision
This is the most recent version of the JavaScript bookmarklet. If you want to see the code, previous versions or a description of why this works, these will be found below.

<a class="btn btn-primary" href="javascript:copyCode()" role="button">Copy the Unblock Code</a>

<script>
    function copyCode() {
        let content = "javascript:(function(){ $('head').append( '<style>' + '#main { height: auto !important } ' + '#article-content.premium-content:before, #article-content.premium-content .ellipsis:after, .article-offer { display: none !important } ' + '</style>' ); $('.paywall').removeClass('paywall'); })();";
        let textarea = document.createElement("textarea");
        textarea.textContent = content;
        document.body.appendChild(textarea);
        textarea.select();
        if (!document.execCommand("copy")) {
            window.prompt("Copy this then click OK",content);
        }
    }
</script>

The button above copies the bookmarklet to your clipboard. Click this and then create a new bookmark (name it what you want) and paste the code copied into the bookmark address.

> On some devices you may find it easier to create a bookmark first with anything and then edit it to insert the code. Make sure the code copied starts with `javascript:` (it will if you copied it using the button).

### How to Use the Bookmarklet
When you're on a NZ Herald premium content page, simply open up your bookmarks and click on the bookmark you created. This will execute the code in the background and un-hide the post content.

> Websites Change: Please note that NZ Herald can change their site at any time, which means this could stop working at any time. If it has stopped working, feel free to comment below and I will look at what has changed.

## Revisions
This is a list of all the revisions of the script. If more information is discovered or the NZ Herald paywall system changes, a new revision will be made. You can copy the script from here if you wish, just make sure to add `javascript:` at the beginning when making it into a bookmark otherwise it will not execute.

### Original Script
The original script does three main things:
 - Display any hidden content that is hidden by the `.paywall` class
 - Hides the fade out of content before the subscription offer and the ellipsis' throughout some articles. 
 - Removes the subscription offer from the page
 
```javascript
(function(){
	$('#article-content.premium-content .paywall').css('display', 'block');
	document.head.insertAdjacentHTML('beforeEnd', '<style>#article-content.premium-content:before, #article-content.premium-content .ellipsis:after {content: none !important}</style>');
	$('.article-offer').css('display', 'none');
})();
```

### Revision 1
Looking in reddit, I found a [post](https://www.reddit.com/r/newzealand/comments/bj9fdu/nz_herald_premium_content_for_free/) that had done the same task I had set out to do. Taking what I found here, I improved the original script and made it easier to read the source.

```javascript
(function(){
    $('head').append(
        '<style>' +
            '#main { height: auto !important }' + 
            '#article-content.premium-content:before, #article-content.premium-content .ellipsis:after, .article-offer { display: none !important }' + // Paywall fix
            // '.pb-f-article-related-articles, .pb-f-global-recommend, .pb-f-global-blank-html { display: none !important }' + // General advertisement removal (I don't include it in the button but you can remove the recommended articles if you wish)
        '</style>'
    );
    $('.paywall').removeClass('paywall'); 
})();
```

## Why Did I Write This?
People asked me to and I put it here for easy access. I don't even read the news.

### And That Shocking Artwork?
I am so sorry. Yes, I used MS Paint.

![Unblock New Zealand Herald Premium Articles Feature Image](/post-assets/unblock-new-zealand-herald-premium-articles/feature.png)
