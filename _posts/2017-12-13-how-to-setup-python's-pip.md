---
layout: post
title: "How To Setup Python's PIP"
date: 2017-12-13
categories: Youtube
tags: Python
---

* content
{:toc}

This tutorial demonstrates how to setup Python's PIP. PIP is a package manager for pip that allows you to download third party modules easily.

{% include embedYouTube.html content="cm6WDGAzDPM" %}

<!-- more -->

## Setting Up
If you haven't used pip before on your computer, go to cmd and type 'pip'. If not errors appear you can move to the next step. If pip is not recognised, you need to set it up. Regarding you actually have python installed (you would not believe some of the comments on this video), open windows explorer (file search) and right click om computer in the side menu.

![Properties for this pc](/images/how-to-setup-python's-pip-demo1.png)

Now click on "Advanced system settings" in the sidebar in the control panel.

![Advanced system settings](/images/how-to-setup-python's-pip-demo2.png)

In the new window, make sure you are in the "Advanced" tab (top) and then click the "Environment Variables" button.

![Advanced tab and environmental variables button](/images/how-to-setup-python's-pip-demo3.png)

In the new window that just appeared, go to the second section - "System variables" and scroll down until you find the "Path" variable. Click on it and then click the edit button below.

![Path variable location](/images/how-to-setup-python's-pip-demo4.png)

Now in the new window, click new on the right and put the folder location of your python scripts folder in. If you don't know where your python scripts folder is can execute this in a python shell or script.

```python
import os
import sys
print (os.path.dirname(sys.executable) + '\Scripts\')

```

![Adding script folder location](/images/how-to-setup-python's-pip-demo5.png)

Now type 'pip' in cmd to make sure you have done this correctly. No errors should appear.

## Usage
You can now use commands like ```pip install pynput``` to install a package or "pip list" to look at all packages installed.

Some useful commands:
- ```pip install [package]```: install a package like pynput or pyinstaller
- ```pip uninstall [package]```: removes an installed package
- ```pip list```: shows install packages
- ```pip show [package]```: shows information about an install package
- ```pip install [package] --upgrade```:  Updates a package

You can find packages from projects on [GitHub](https://github.com/) or [PyPI](https://pypi.python.org/pypi).

## FAQ
If you have any questions, please go to the video at the top of this article and leave a comment. I aim to reply in less than two days.

### When I try to edit the path value it just shows the path name and value, not the full list
You are using Windows 10 (this is fine!). Just put a semicolon at the end (';') and then put the path (no space between them).
