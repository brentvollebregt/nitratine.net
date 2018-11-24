title: "Media Picker"
date: 2018-07-15
category: Projects
tags: [Python, Images]
feature: interface.jpg
description: "I had been requested to help someone with filtering a lot of images taken with a camera. This would need to occur regularly so I created an interface that would help them easily select what photos they wanted."

*Easily chose which images to keep with a simple interface.*

I had been requested to help someone with filtering a lot of images taken with a camera. This would need to occur regularly so I created an interface that would help them easily select what photos they wanted. After they have selected and moved their images, they are then free to delete the original files/folders if wanted.

![Interface](/post-assets/media-picker/interface.jpg)

{% with repo="brentvollebregt/media-picker" %}{% include 'blog-post-addGitHubRepoBadges.html' %}{% endwith %}

This project is a Flask server hosted by Python that is designed to be opened in a Chrome window. Other browsers will work but due to layouts, images of different sizes will mess with the display.

## Features
 - Add files by file, files or folder
 - Simple "Copy" or "Don't Copy" buttons to determine what to keep
 - Can easily clear the currently selected files or choices
 - Easily clear the selected choices
 - Export selections by copy or move
 - Clicking on the image (in the centre) will enlarge it
 - Clicking to the right/left of the image will go to the next corresponding image
 - View all images in a scrollable bar at the bottom
 - Server will close itself when it detects that there is no more activity

## Getting Started

### Prerequisites
 - Python : Python 2.7, 3.4 - 3.6
 - Chrome : to run the user interface

### Instillation
1. Clone/download the repo at [github.com/brentvollebregt/media-picker](https://github.com/brentvollebregt/media-picker)
2. Open cmd/terminal and cd to the project
3. Execute pip install -r requirements.txt

### Usage
Execute ```run.py``` by either calling it as an argument with Python, in IDLE or double clicking on it. Chrome should open and display the interface.

Click the blue "Add Files" button and add your desired files. Use the red/green button to select what images to keep and then click export when you have finished your selection (you do not need to select all the images to do this, blue will be ignored like red).
