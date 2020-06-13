---
templateKey: blog-post
title: "How To Setup Python's PIP"
date: 2017-12-13T12:00:00.000Z
category: YouTube
tags: [python]
image: demo5.png
description: "This tutorial demonstrates how to set up Python's PIP. PIP is a package manager for pip that allows you to download third-party modules easily. I explain how to find your scripts folder and how to find pip."
disableToc: false
hidden: false
youtubeVideoId: cm6WDGAzDPM
---

## Setting Up

If you haven't used pip before on your computer, go to cmd and type 'pip'. If not errors appear you can move to the next step. If pip is not recognised, you need to set it up. Regarding you have python installed (you would not believe some of the comments on this video), open windows explorer (file search) and right-click on computer in the side menu.

![Properties for this pc](demo1.png)

Now click on "Advanced system settings" in the sidebar in the control panel.

![Advanced system settings](demo2.png)

In the new window, make sure you are in the "Advanced" tab (top) and then click the "Environment Variables" button.

![Advanced tab and environmental variables button](demo3.png)

In the new window that just appeared, go to the second section - "System variables" and scroll down until you find the "Path" variable. Click on it and then click the edit button below.

![Path variable location](demo4.png)

Now in the new window, click new on the right and put the folder location of your python scripts folder in. If you don't know where your python scripts folder is can execute this in a python shell or script.

```python
import os
import sys
print (os.path.dirname(sys.executable) + '\Scripts\\')
```

![Adding script folder location](demo5.png)

Now type 'pip' in cmd to make sure you have done this correctly. No errors should appear.

> If you are using an older version of Windows, you will be presented with a one-line input field. Add a semicolon ';' to the end of the text current in the field and then add the path as you would have in the area before. `<current text>;<path>`

## A Shortcut

A while ago I made a script that automatically sets up the `python` and `pip` commands on Windows by putting their directories on the users PATH variable automatically.

You can find this script in my ["Fix: 'python' is not recognized as an internal or external command"](/blog/post/fix-python-is-not-recognized-as-an-internal-or-external-command/) post.

## Usage

You can now use commands like `pip install pynput` to install a package or "pip list" to look at all packages installed.

Some useful commands:

- `pip install [package]`: install a package like pynput or pyinstaller
- `pip uninstall [package]`: removes an installed package
- `pip list`: shows install packages
- `pip show [package]`: shows information about an install package
- `pip install [package] --upgrade`: Updates a package

You can find packages from projects on [GitHub](https://github.com/) or [PyPI](https://pypi.python.org/pypi).

## Common Issues and Questions

### When editing the PATH variable, I can only edit the variable

Add a ';' to the end and then put in the folder location, then apply/save it. This input is like this because you are using an older version of Windows.

### It Still Isn't Working

Regarding you followed the instructions properly, this will work. One other method to call pip is by calling `python -m pip`. Using this allows us to call pip when the scripts folder is not in the PATH variable. Note that the directory of python.exe must be in the PATH variable for this to work (which means calling `python` in cmd must work first).
