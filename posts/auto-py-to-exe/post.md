title: "Auto Py To Exe"
date: 2018-03-10
category: Projects
tags: [python, pyinstaller, eel, gui]
feature: feature.png
description: "This project allows you to convert python scripts to executables with a simple interface. The interface uses chromes app mode and lists all possible flags for pyinstaller. The whole idea seems automatic as it cleans up after itself."
github: brentvollebregt/auto-py-to-exe

[TOC]

## What is this?
This application displays a simple interface that allows you to convert .py to .exe easily. By just selecting the file, if you want it to convert to onefile and if you want a console, you will only need to press convert and wait for the script to do the rest.

<div markdown="1" style="text-align: center">

![Empty interface](/posts/auto-py-to-exe/feature.png)

The script is built using [Eel](https://github.com/ChrisKnott/Eel) and uses [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/index.html) to convert the script

</div>

<div style="text-align: center">
    <a href="https://pypi.org/project/auto-py-to-exe/"><img class="mt-1" style="display: inline;" src="https://img.shields.io/pypi/v/auto-py-to-exe.svg" alt="PyPI Version"></a>
    <a href="https://pypi.org/project/auto-py-to-exe/"><img class="mt-1" style="display: inline;" src="https://img.shields.io/pypi/pyversions/auto-py-to-exe.svg" alt="PyPI Supported Versions"></a>
    <a href="https://pypi.org/project/auto-py-to-exe/"><img class="mt-1" style="display: inline;" src="https://img.shields.io/pypi/l/auto-py-to-exe.svg" alt="License"></a>
    <a href="https://pepy.tech/project/auto-py-to-exe"><img class="mt-1" style="display: inline;" src="https://pepy.tech/badge/auto-py-to-exe" alt="Downloads"></a>
    <a href="https://pepy.tech/project/auto-py-to-exe"><img class="mt-1" style="display: inline;" src="https://img.shields.io/pypi/dm/auto-py-to-exe.svg" alt="Downloads Per Month"></a>
    <a href="https://pyinstaller.readthedocs.io/en/stable/requirements.html"><img class="mt-1" src="https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey" alt="Supported Platforms"></a>
</div>

## Demo

![auto-py-to-exe Demo](/posts/auto-py-to-exe/auto-py-to-exe-demo.gif)

## Getting Started

### Prerequisites

- Python: 3.6-3.12

_To have the interface displayed in the images, you will need Chrome. If Chrome is not installed or `--no-chrome` is passed, the default browser will be used._


### Installing via [PyPI](https://pypi.org/project/auto-py-to-exe/)

You can install this project using PyPI:

```
$ pip install auto-py-to-exe
```

Then to run it, execute the following in the terminal:

```
$ auto-py-to-exe
```

> If you have more than one version of Python installed, you can use `python -m auto_py_to_exe` instead of `auto-py-to-exe`.

### Installing via [GitHub](https://github.com/brentvollebregt/auto-py-to-exe)

```
$ git clone https://github.com/brentvollebregt/auto-py-to-exe.git
$ cd auto-py-to-exe
$ python setup.py install
```

Then to run it, execute the following in the terminal:

```
$ auto-py-to-exe
```

## Using the Application

1. Select your script location (paste in or use a file explorer)
   - The outline will become blue if the file exists
2. Select other options and add things like an icon or other files
3. Click the big blue button at the bottom to convert
4. Find your converted files in /output when completed

_Easy._

## Examples

The [examples/](https://github.com/brentvollebregt/auto-py-to-exe/tree/master/examples/) directory offers some examples of how to write your scripts and package them with auto-py-to-exe.

- [Basic (console application)](https://github.com/brentvollebregt/auto-py-to-exe/tree/master/examples/1-basic/readme.md)
- [No Console (as typically desired for GUI-based applications)](https://github.com/brentvollebregt/auto-py-to-exe/tree/master/examples/2-no-console/readme.md)
- [Images and other non-.py files (static files to be included)](https://github.com/brentvollebregt/auto-py-to-exe/tree/master/examples/3-images-and-other-non-py-files/readme.md)
- [Persistent data (like databases)](https://github.com/brentvollebregt/auto-py-to-exe/tree/master/examples/4-persistent-data/readme.md)

## Video

If you need something visual to help you get started, [I made a video for the original release of this project](https://youtu.be/OZSZHmWSOeM); some things may be different but the same concepts still apply.

## Contributing

Check out [CONTRIBUTING.md](https://github.com/brentvollebregt/auto-py-to-exe/blob/master/CONTRIBUTING.md) to see guidelines on how to contribute. This outlines what to do if you have a new feature, a change, translation update or have found an issue with auto-py-to-exe.

## Issues Using the Tool

If you're having issues with the packaged executable or using this tool in general, I recommend you read [my blog post on common issues when using auto-py-to-exe](https://nitratine.net/blog/post/issues-when-using-auto-py-to-exe/?utm_source=auto_py_to_exe&utm_medium=readme_link&utm_campaign=auto_py_to_exe_help). This post covers things you should know about packaging Python scripts and fixes for things that commonly go wrong.

If you believe you've found an issue with this tool, please follow the ["Reporting an Issue" section in CONTRIBUTING.md](https://github.com/brentvollebregt/auto-py-to-exe/blob/master/CONTRIBUTING.md#reporting-an-issue).

## Screenshots


<div markdown="1" style="display: grid; grid-template-columns: 1fr 1fr; grid-gap: 6px">

[![Empty interface](/posts/auto-py-to-exe/empty-interface.png)](/posts/auto-py-to-exe/empty-interface.png)

[![Filled out](/posts/auto-py-to-exe/filled-out.png)](/posts/auto-py-to-exe/filled-out.png)

[![Converting](/posts/auto-py-to-exe/converting.png)](/posts/auto-py-to-exe/converting.png)

[![Completed](/posts/auto-py-to-exe/completed.png)](/posts/auto-py-to-exe/completed.png)
    
</div>

## Response
I really wanted to get this project out there so I released a YouTube video demonstrating how to set up and use the interface (video above). A day later I made a post in the /r/Python subreddit titled ["Auto Py to Exe is Complete"](https://www.reddit.com/r/Python/comments/84kwb8/auto_py_to_exe_is_complete/).
To my surprise, the next morning (about 7 hours) I had more than 300 upvotes which to me was a big thing. I had many replies which I took time to read and reply to. About 44 hours later the post finally lost its top place on the subreddit and the post is sitting at 454 points with 12.1k views and 75 comments.
I can't believe how big this got and it means a lot to me when I saw people thanking me for the project. When a couple of issues came to the Github repo I realised people do care about this and I was quick to fix these.
Once again, thank you for the support; I loved making this project.
