---
layout: post
title: "Multi Clipboard"
date: 2017-12-20
categories: Projects
tags: Python Clipboard GUI
---

* content
{:toc}

A simple clipboard manager so you will never find yourself copying the same thing twice. Images, text and files are supported and unlimited amounts of saved clipboards can be created. Switch clipboard contents using easy commands and a clean UI. Built in Python using PYQT5, pywin32 and PIL. The idea of this is to easily switch keyboards with simple commands. Map commands to keys to use this easily.

[Find the project on GitHub](https://github.com/brentvollebregt/mutli-clipboard)

## What is this?
This is a python script which allows you to swap clipboard contents to a type of storage so you don't have to go back and copy something because you just temporarily copied something. The idea of this is to act like a hotbar like in games. The main feature of this project is the GUI but there is support for command line manipulation.

## Demonstration and Screenshots
![GUI example](/images/multi-clipboard-gui1.jpg)

<!-- more -->

## Installation and Setup
1. Install PIL if you are using Python 3 ( ```pip install Pillow``` )
2. Install PYQT5 ( ```pip install pyqt5``` )
3. Install pywin32 ( ```pip install pypiwin32``` or [Installer](https://sourceforge.net/projects/pywin32/files/pywin32/))

## Usage
### GUI Usage
Use ```clipboards.py view``` to open the GUI
- Click on clipboard to switch to it (auto close feature mentioned below)
- Right click menu on each clipboard
- Clear all clipboards option
- Easy refresh
- Can add from the GUI (will pick the lowest integer)
- Displays both text and images

### Command Line Usage
- ```clipboards.py view``` - Opens GUI (as stated above)
- ```clipboards.py view 1``` - Views clipboard 1
- ```clipboards.py switch [clipboard]``` - Will switch current clipboard to the clipboard specified
- ```clipboards.py clear``` - Clear all clipboards
- ```clipboards.py clear 1``` - Clear clipboard 1

#### Examples
Command -> ```clipboards.py switch 1``` : Switching to current clipboard
Clipboard is saved under current id and clipboard doesn't change

|Current Clipboard ID|Storage|Clipboard|
|--- |--- |--- |
|Before|1|1: 123, 2: abc|myclipboard|
|After|1|1: myclipboard, 2: abc|myclipboard|

Command -> ```clipboards.py switch 2``` : Switching to a different clipboard
Clipboard is saved under current id, then clipboard 2 is put into the clipboard and the current clipboard is set to 2

|Current Clipboard ID|Storage|Clipboard|
|--- |--- |--- |
|Before|1|1: 123, 2: abc|myclipboard|
|After|2|1: myclipboard, 2: abc|abc|

Command -> ```clipboards.py switch 3``` : Switching to a clipboard that doesn't exist
Clipboard is saved under current id and clipboard doesn't change. Clipboard id is 3 and will be created when it is switched next time

|Current Clipboard ID|Storage|Clipboard|
|--- |--- |--- |
|Before|1|1: 123, 2: abc|myclipboard|
|After|3|1: myclipboard, 2: abc|myclipboard|

Clipboards can be named more than just numbers.
## Options
Options can be found in the data.json file.
- Close GUI when a clipboard is selected - data.json:close_on_gui_select
- Keep window on top until closed - data.json:stay_on_top
- Display HTML as plain text instead of rendering it in the GUI - found in data.json:html_as_plain_text
- Opacity of GUI - found in data.json:opacity

## Features
- Dark stylesheet and transparency
- Dynamically displays contents of clipboards
- Will save current clipboard on startup (so you can see what the state it would be if it is switched)
- Can view all clipboard contents easily
- Easily add and remove clipboards

## Thanks To
- [Michael Robertson](https://github.com/MBRobertson) for adding file support.

