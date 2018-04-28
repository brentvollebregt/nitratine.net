---
layout: post
title: "Code Background in HTML"
date: 2018-01-24
categories: Tutorials
tags: HTML CSS
---

* content
{:toc}

This HTML code displays a code background which can be used in images and as a general theme.

## What is this?
Recently I created a new YouTube channel art and wanted to be a bit creative. Knowing that there is a lot of space that can be used above and below the main area of the image shown on pc, tablet and mobile for tv, I wanted to use this space. I wanted to put some sort of coloured code as a background; the best language to use in my opinion was JavaScript as it is very compressible compared to python which relies on whitespace and indentation heavily.

A small sample of what I created is shown below. The script covers the full page and the size can easily be changed.

![Background Code Example](/images/code-background-in-html/example1.png)

<!-- more -->

## Setting the Script Up
First create a new .html file and save it. Now enter the code in below.

```html
<html>
    <head>
            <style>
            </style>
    </head>
    <body>
    </body>
</html>
```

Now in the <style> tag enter the css:

```css
body {overflow: hidden;margin: 0;background: #263238;}
pre {white-space: normal;}
.highlight {word-break: break-all; font-size: 12px;}
.highlight .c,.highlight .c1,.highlight .cm,.highlight .cp,.highlight .cs{color:#75715e}
.highlight .err{color:#960050;background-color:#1e0010}
.highlight .k{color:#66d9ef}
.highlight .l{color:#ae81ff}
.highlight .n{color:#f8f8f2}
.highlight .o{color:#f92672}
.highlight .p{color:#f8f8f2}
.highlight .ge{font-style:italic}
.highlight .gs{font-weight:700}
.highlight .kc,.highlight .kd{color:#66d9ef}
.highlight .kn{color:#f92672}
.highlight .kp,.highlight .kr,.highlight .kt{color:#66d9ef}
.highlight .ld{color:#e6db74}
.highlight .m{color:#ae81ff}
.highlight .s{color:#e6db74}
.highlight .na{color:#a6e22e}
.highlight .nb{color:#f8f8f2}
.highlight .nc{color:#a6e22e}
.highlight .no{color:#66d9ef}
.highlight .nd{color:#a6e22e}
.highlight .ni{color:#f8f8f2}
.highlight .ne,.highlight .nf{color:#a6e22e}
.highlight .nl,.highlight .nn{color:#f8f8f2}
.highlight .nx{color:#a6e22e}
.highlight .py{color:#f8f8f2}
.highlight .nt{color:#f92672}
.highlight .nv{color:#f8f8f2}
.highlight .ow{color:#f92672}
.highlight .w{color:#f8f8f2}
.highlight .mf,.highlight .mh,.highlight .mi,.highlight .mo{color:#ae81ff}
.highlight .s2,.highlight .sb,.highlight .sc,.highlight .sd{color:#e6db74}
.highlight .se{color:#ae81ff}
.highlight .s1,.highlight .sh,.highlight .si,.highlight .sr,.highlight .ss,.highlight .sx{color:#e6db74}
.highlight .bp,.highlight .vc,.highlight .vg,.highlight .vi{color:#f8f8f2}
.highlight .il{color:#ae81ff}
.highlight .gu{color:#75715e}
.highlight .gd{color:#f92672}
.highlight .gi{color:#a6e22e}
```

This CSS has been comes with the [pygments](http://pygments.org/) library; I use it in this website. I have compressed and formatted it to make the code look a bit more appealing and smaller. I also added a couple of extra classes for wrapping, backgrounds and to stop scrolling.

## The Script
Now if you thought the CSS was big, wait for the JavaScript. For this project I needed a sufficient amount of JavaScript. I decided on using the jQuery source code as it is large enough to fill a screen. I used the [compressed, production jQuery 3.3.1](https://code.jquery.com/jquery-3.3.1.min.js). Go to that link and copy all the code using Ctrl + A, Ctrl + C.

Now go to my highlighter tool at [/tools/pygments-online](http://nitratine.pythonanywhere.com/tools/pygments-online) and paste the code in the "Input Code" box. Change the code to "JavaScript" and click highlight.

This may take a few seconds but you should see an output like this:

![Highlighted JavaScript Example](/images/code-background-in-html/example2.png)

Click on the "Copy to Clipboard" button and put this straight into the <body> tag.

Now open the .html file in chrome and you will see that the whole background is code.

![Final Example](/images/code-background-in-html/final.png)

## Modifications
If you want to make this code scroll, remove "overflow: hidden;" in the body css selector.

If you want to change the font size, change "font-size: 12px;" in the highlight class.

If you want to change the background colour, change it in the body css selector.

If you want to make this code a background, you can either take a screenshot of it or style the highlight class with {position: absolute; top: 0; left: 0; z-index: -100;} as shown [here](https://stackoverflow.com/questions/25970787/use-a-div-as-a-background-for-another-element)

## Sources
- [jquery.com for javascript code](https://jquery.com/)

