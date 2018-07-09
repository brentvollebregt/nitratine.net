---
layout: post
title: "Putting auto-py-to-exe on PyPI"
date: 2018-09-05
categories: General
tags: Python PyPI
description: "I have finally decided to put auto-py-to-exe on the Python Package Index. Auto-py-to-exe can now be installed using pip by executing 'pip' install auto-py-to-exe."
---

* content
{:toc}

I have finally decided to put [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) on the [Python Package Index](https://pypi.org/). Auto-py-to-exe can now be installed using pip by executing the following in the terminal:

```
$ python -m pip install auto-py-to-exe
```

Then to run it, you can simply call it in the terminal:

```
$ auto-py-to-exe
```

And as the original, you can still pass a file to pre-fill the script you want to package:

```
$ auto-py-to-exe my_script.py
```

<p align="center">
    <img src="https://img.shields.io/pypi/v/auto-py-to-exe.svg" alt="PyPI Version">
    <img src="https://img.shields.io/pypi/pyversions/auto-py-to-exe.svg" alt="PyPI Supported Versions">
    <img src="https://img.shields.io/pypi/l/auto-py-to-exe.svg" alt="License">
</p>

<!-- more -->

## General Talk About the Process

I decided to create a [new repository](https://github.com/brentvollebregt/auto-py-to-exe-pypi) for the package that would be [hosted on PyPI](https://pypi.org/project/auto-py-to-exe/) as the video that I provided will still help people understand what is going on. In the old repo I have provided a link to the new one and added in the instructions for instillation using pip.

It took me a few hours to find out how to structure my package and have everything setup properly from the readme to the entry-points.

I use a lot of resources for finer details and looked at a lot of setup.py files but these resources would have been the most helpful:
- [Analyzing PyPI package downloads](https://packaging.python.org/guides/analyzing-pypi-package-downloads/)
- [Publishing your First PyPI Package by/for the Absolute Beginner](https://jonemo.github.io/neubertify/2017/09/13/publishing-your-first-pypi-package/)
- [GitHub/kennethreitz/setup.py](https://github.com/kennethreitz/setup.py)

### Issues With Entry-points
One issue I sat on for a bit was an error message saying *EntryPoint must be in 'name=module:attrs [extras]' format*. I had provided *auto-py-to-exe=auto-py-to-exe.\_\_main\_\_:run* which followed the pattern provided.

I had completely forgotten though that when importing packages normally in Python, hyphens cause a lot of issues. To fix this I initially changed all traces of 'auto-py-to-exe' to 'auto_py_to_exe'. I later found out that I could still keep the package name 'auto-py-to-exe' by setting name='auto-py-to-exe' and setting everything else (including the folder name) to 'auto_py_to_exe'; a small price to pay for the name.

So to take from this: hyphens < underscore in package names.

### Issues With README
The next issue was with PyPI's Warehouse itself (afterwards). I wanted to render my README in PyPI but it wasn't doing it for some reason. I had later found that when looking at the [setup.py for Eel](https://github.com/ChrisKnott/Eel/blob/master/setup.py) I had thought it was a great idea to take the long_description value being set to `open('README.md', encoding='utf-8').readlines()[1]`. I thought very little about this and in the end actually decided to test it and found that it was only taking the first line from my README; copy and pasting is dangerous.

Next was the fact that you needed a version of setup tools that was waaaay higher than what I had; a simple fix of course using `pip install setuptools --upgrade`.

Lastly I had to add `long_description_content_type='text/markdown'` to setup.py but in all honesty did it in the middle of trying to solve the above two issues so am not 100% sure if this actually changed anything.

Lesson to take from this; know what you're copying and StackOverflow is very helpful (as I didn't already know that...)
