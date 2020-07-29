title: "Auto Py To Exe"
date: 2018-03-10
category: Projects
tags: [python, pyinstaller, eel, gui]
feature: feature.png
description: "This project allows you to convert python scripts to executables with a simple interface. The interface uses chromes app mode and lists all possible flags for pyinstaller. The whole idea seems automatic as it cleans up after itself."
github: brentvollebregt/auto-py-to-exe

## What is this?
This application displays a simple interface that allows you to convert py to exe easily. By just selecting the file, if you want it to convert to onefile and if you want a console, you will only need to press convert and wait for the script to do the rest.

<div style="text-align: center">
	<img src="/posts/auto-py-to-exe/feature.png" alt="Empty interface"/>
	<p>The script is built using <a class="link" href="https://github.com/ChrisKnott/Eel">Eel</a> and uses <a href="https://www.pyinstaller.org/">PyInstaller</a> to convert the script.</p>
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

<video style="width:90%;height:auto;margin:auto;display:block;" controls="" class="mb-3">
    <source src="/posts/auto-py-to-exe/auto-py-to-exe-demo.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

## Getting Started

### Prerequisites
 - Python : Python 2.7 / 3.5-3.7 (see [here](https://github.com/pyinstaller/pyinstaller/issues/4311) for 3.8)

*To have the interface displayed in the images, you will need chrome. If chrome is not installed or --no-chrome is supplied, the default browser will be used.*

### Installation and Usage
#### Installing Via [PyPI](https://pypi.org/project/auto-py-to-exe/)
You can install this project using PyPI:
```
$ pip install auto-py-to-exe
```
Then to run it, execute the following in the terminal:
```
$ auto-py-to-exe
```

### Installing Via [GitHub](https://github.com/brentvollebregt/auto-py-to-exe)
```
$ git clone https://github.com/brentvollebregt/auto-py-to-exe.git
$ cd auto-py-to-exe
$ python setup.py install
```
Then to run it, execute the following in the terminal:
```
$ auto-py-to-exe
```

#### Running Locally Via [Github](https://github.com/brentvollebregt/auto-py-to-exe) (no install)
You can run this project locally by following these steps:
1. Clone/download the [repo](https://github.com/brentvollebregt/auto-py-to-exe)
2. Open cmd/terminal and cd into the project
3. Execute ```python -m pip install -r requirements.txt```

Now to run the application, execute ```python -m auto_py_to_exe```. A Chrome window in app mode will open with the project running inside.

> Make sure you are in the directory below auto_py_to_exe (you will be after step 3) when calling `python -m auto_py_to_exe` or you will need to reference the folder auto_py_to_exe absolutely/relatively to where you currently are.

## Using the Application
1. Select your script location (paste in or use a file explorer)
    - Outline will become blue when file exists
2. Select other options and add things like an icon or other files
3. Click the big blue button at the bottom to convert
4. Find your converted files in /output when completed

*Easy.*

### Arguments
Usage: `auto-py-to-exe [-nc] [-c [CONFIG]] [filename]`

| Argument                       | Type       | Description                                                                                         |
|--------------------------------|------------|-----------------------------------------------------------------------------------------------------|
| filename                       | positional | Pre-fill the "Script Location" field in the UI.                                                     |
| -nc, --no-chrome               | optional   | Open the UI using the default browser (which may be Chrome). Will not try to find Chrome            |
| -c [CONFIG], --config [CONFIG] | optional   | Provide a configuration file (json) to pre-fill the UI. These can be generated in the settings tab. |
| -o [PATH], --output-dir [PATH] | optional   | Set the default output directory. This can still be changed in the ui.                              |

> If you are running this package locally, you will need to call ```python -m auto_py_to_exe``` instead of ```auto-py-to-exe```

### Configurations
Instead of inserting the same data into the UI over and over again, you can export the current state of the UI by going to the section "Configuration Import and Export" at the bottom of the advanced tab and exporting a JSON string to the clipboard or a file. This can then be imported into the UI again to re-populate all fields.

## Video
If you need something visual to help you get started, [I made a video for the original release of this project](https://youtu.be/OZSZHmWSOeM); some things may be different but the same concepts still apply.

## Issues Using the Tool
If you're having issues with the packaged executable or using this tool in general, I recommend you read [my blog post on common issues when using auto-py-to-exe](https://nitratine.net/blog/post/issues-when-using-auto-py-to-exe/). This post covers things you should know about packaging Python scripts and fixes for things that commonly go wrong.

## Screenshots

<div style="display: grid; grid-template-columns: 1fr 1fr; grid-gap: 6px;">
    <a href="/posts/auto-py-to-exe/empty-interface.png"><img src="/posts/auto-py-to-exe/empty-interface.png" alt="Empty interface" /></a>
    <a href="/posts/auto-py-to-exe/filled-out.png"><img src="/posts/auto-py-to-exe/filled-out.png" alt="Filled out" /></a>
    <a href="/posts/auto-py-to-exe/converting.png"><img src="/posts/auto-py-to-exe/converting.png" alt="Converting" /></a>
    <a href="/posts/auto-py-to-exe/completed.png"><img src="/posts/auto-py-to-exe/completed.png" alt="Completed" /></a>
</div>

## Response
I really wanted to get this project out there so I released a YouTube video demonstrating how to set up and use the interface (video above). A day later I made a post in the /r/Python subreddit titled ["Auto Py to Exe is Complete"](https://www.reddit.com/r/Python/comments/84kwb8/auto_py_to_exe_is_complete/).
To my surprise, the next morning (about 7 hours) I had more than 300 upvotes which to me was a big thing. I had many replies which I took time to read and reply to. About 44 hours later the post finally lost its top place on the subreddit and the post is sitting at 454 points with 12.1k views and 75 comments.
I can't believe how big this got and it means a lot to me when I saw people thanking me for the project. When a couple of issues came to the Github repo I realised people do care about this and I was quick to fix these.
Once again, thank you for the support; I loved making this project.
