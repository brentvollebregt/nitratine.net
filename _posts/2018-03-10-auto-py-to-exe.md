---
layout: post
title: "Auto Py To Exe"
date: 2018-03-10
categories: Projects
tags: Python pyinstaller Eel GUI
description: "This project allows you to convert python scripts to executables with a simple interface. The interface uses chromes app mode and lists all possible flags for pyinstaller. The whole idea seems automatic as it cleans up after itself."
---

* content
{:toc}

This project allows you to convert python scripts to executables with a simple interface. The interface uses chromes app mode and lists all possible flags for pyinstaller.

{%- include addGitHubRepoBadges.html content="brentvollebregt/auto-py-to-exe" -%}

## What is this?
This application displays a simple interface that allows you to convert py to exe easily. By just selecting the file, if you want it to convert to onefile and if you want a console, you will only need to press convert and wait for the script to do the rest.

<div style="text-align: center">
	<img src="https://i.imgur.com/EuUlayC.png" alt="Empty interface"/>
	<p>The script is built using <a class="link" href="https://github.com/ChrisKnott/Eel">Eel</a> and uses <a href="http://www.pyinstaller.org/">PyInstaller</a> to convert the script.</p>
</div>

<!-- more -->

## Getting Started
### Prerequisites
 - Python : Python 2.7, 3.3 - 3.6

*To have the interface displayed in the images, you will need chrome. If chrome is not installed or --no-chrome is supplied the default browser will be used.*

### Instillation and Usage
#### Via [PyPI](https://pypi.org/project/auto-py-to-exe/)
You can install this project using the PyPI:
```
$ pip install auto-py-to-exe
```
Now to run it, execute the following in the terminal:
```
$ auto-py-to-exe
```

#### Via [The GitHub Repository](https://github.com/brentvollebregt/auto-py-to-exe)
You can install this project using this repository by following these steps:
1. Clone/download the repo at [github.com/brentvollebregt/auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe)
2. Open cmd/terminal and cd to the project
3. Execute ```pip install -r requirements.txt```

Now to run the application, run the ```run.py``` file with python. A Chrome will open in app mode with the project running inside.

## Using the Application
1. Select your script location (paste in or use a file explorer)
    - Outline will become blue when file exists
2. Select other options and add things like an icon or other files
3. Click the big blue button at the bottom to convert
4. Find your converted files in /output when completed

*Easy.*

### Arguments
Alternatively you can execute ```python run.py [filename]```. This will open up the window with the filename in the script location.

You can also pass ```--no-chrome``` if you want to use your default browser and not chromes app mode; for example ```python run.py --no-chrome my_script.py```.

> If you installed this package using pip you can call ```auto-py-to-exe``` instead of ```python run.py```

## Video
If you need something visual to help you get started, I made a video for the original release of this project, some things may be different but the same concepts still apply.

{%- include embedYouTube.html content="OZSZHmWSOeM" -%}

## Looking for the PyPI Version?
If you are looking for the PyPI version of this repo, go to [auto-py-to-exe-pypi](https://github.com/brentvollebregt/auto-py-to-exe-pypi). The original repo has been preserved to keep in line with the provided video but instructions have been provided to use the new method.

## Screenshots
![Empty interface](https://i.imgur.com/dd0LC2n.png)

![Filled out](https://i.imgur.com/Wd9pFqR.png)

![Converting](https://i.imgur.com/MjdONcC.png)

## Response
I really wanted to get this project out there so I released a YouTube video demonstrating how to setup and use the interface (video above). A day later I made a post in the /r/Python sub reddit titled ["Auto Py to Exe is Complete"](https://www.reddit.com/r/Python/comments/84kwb8/auto_py_to_exe_is_complete/).
To my surprisement the next morning (about 7 hours) I had more than 300 upvotes which to me was a big thing. I had many replies which I took time to read and reply to. About 44 hours later the post finally lost it's top place on the subreddit and the post is sitting at 454 points with 12.1k views and 75 comments.
I can't believe how big this got and it means a lot to me when I saw people thanking me for the project. When the couple of issues came to the Github repo I realised people do care about this and I was quick to fix these.
Once again, thank you for the support; I loved making this project.

*Updated 07-08-18*
