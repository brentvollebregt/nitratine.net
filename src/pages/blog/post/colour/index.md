---
templateKey: blog-post
title: "Colour"
date: 2017-11-18T00:00:00.000+12:00
category: Apps
tags: [android, java]
image: feature.png
description: "This app is based off a goal of obtaining all 16,777,216 colours by randomly generating colours when taping the screen. This figure is the number of colours a screen can display today and it's your challenge to find them all."
disableToc: true
hidden: false
---

<youtube-video id="x56o7b9Uor8"></youtube-video>

<a href="https://play.google.com/store/apps/details?id=com.pythonanywhere.brentvollebregt.colour" style="display: block; max-width: 200px; margin: auto;">
    <img src="./google-play.png" alt="Get it on Google Play" style="height: 60px;"/>
</a>

## The Idea

One night I was having a chat with a friend on how stupid apps always seem to make it to the top. We started to think of stupid apps and thus this app was born. Based on the simple idea of just tapping the screen to randomly generate colours I managed to turn an idea into an app in a couple of months in between my study.
This idea also made me wonder how long would it take to complete an app of this nature for users? The investigation can be found [here](/blog/post/randomly-generating-numbers-to-fulfil-an-integer-range/).

## The Goal

So the app has a pretty simple goal; find all the colours. Now it may seem that all you have to do is tap the screen 16,777,216 times to finish but colours are randomly generated. This means if you did get to 16,777,215 colours, you would have a 1 in 16,777,216 of finishing.
On the chance that you get two of one colour, you can merge it with another duplicate colour you have in the colour mixer to find another colour.

## Screenshots

<div style="display: grid; grid-template-columns: repeat(4, 1fr); grid-gap: 3px;" class="mb-3">
    <div><img src="./tap-screen.png" alt="Main screen"/></div>
    <div><img src="./colour-viewer.png" alt="Colour finder"/></div>
    <div><img src="./colour-mixer.png" alt="Colour mixer"/></div>
    <div><img src="./previous-colours.png" alt="Recent colours"/></div>
</div>

## Features

- Recent Colours: Hold down on the tap screen on swipe to the right to look at the 10 most recent colours found
- View Colours: Look at the colours you currently have
- Status: On the tap screen your taps, progress and current colour count are displayed
- Mix Colours: When you find duplicates of colours, mix them to find a new colour
- Achievements: Get milestone achievements as you play
- Gestures: Swipe to get to different areas of the app (can be toggled)

## Bug Reporting and Feedback

Think you've found a bug or just want to give back some feedback? Send me an [email](mailto:////brent@nitratine.net?subject=Colour%20Bug%20Report) and I'll look into it!
For bug reports please include:

- Your name
- Model of your phone
- Android version
- A summary of the bug
- How you found the bug (how to reproduce it)

## Other Projects Used

- [github.com/chiralcode/Android-Color-Picker](https://github.com/chiralcode/Android-Color-Picker)
- [github.com/balysv/material-ripple](https://github.com/balysv/material-ripple)
- [materialdesignicons.com](https://materialdesignicons.com)
- [material.io/icons/](https://material.io/icons/)
