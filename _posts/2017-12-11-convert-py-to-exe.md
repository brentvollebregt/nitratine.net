---
layout: post
title: "Convert .py to .exe"
date: 2017-12-11
categories: Youtube
tags: Python pyinstaller
description: "A demonstration of how to package a python script into an executable file. This tutorial includes compiling to one file, no console, how to add an icon and adding other files to the final package."
---

* content
{:toc}

A demonstration of how to package a python script into an executable file. This tutorial includes compiling to one file, no console, how to add an icon and adding other files to the final package.

{% include embedYouTube.html content="lOIJIk_maO4" %}

<!-- more -->

## PIP
If you haven't used or setup pip before, go to my tutorial at [{% link _posts/2017-12-13-how-to-setup-pythons-pip.md %}]({{ site.baseurl }}{% link _posts/2017-12-13-how-to-setup-pythons-pip.md %}) to setup pip.

## Pyinstaller
Now that pip has been setup, execute the command ```pip install pyinstaller``` in cmd. Make sure to check the output for errors as if there are errors it would not have installed successfully. Note pyinstaller doesn't support all versions of Python. As of 11-12-17 pyinstaller supports up to Python 3.6. You can check at [http://www.pyinstaller.org/downloads.html](http://www.pyinstaller.org/downloads.html) under Downloads -> Release to see what is supported by the latest release.

To make sure it installed properly, type ```pyinstaller``` in cmd and make sure no errors appeared.

![pyinstaller command output](/images/convert-.py-to-.exe/demo6.png)
## Basic Compiling
Created a new folder and put your python file in it and any other modules or files it may need. Then hold shift and right click in the folder, in the menu that popped up, click "Open PowerShell Window Here" or "Open command window here" for older versions of windows. If this option doesn't appear, try again or open cmd and type ```cd {folder location}``` to move to that folder.

![Open PowerShell window here](/images/convert-.py-to-.exe/demo7.png)

Now that cmd is in the right location, execute ```pyinstaller {the name of your python file}``` make sure to add .py or whatever extension it has. Wait for it to finish and check if any errors have appeared. If none have you can close cmd and look at the three folders generated.

Look in the 'dist' folder and you should see {the name of your script}.exe. If you run that your script should execute as an exe.

## No Console
When running the compiled script, you will notice a console window will appear. If you do not want this, add the 'w' flag to the statement when creating the script.

Thus the new statement will be ```pyinstaller -w {the name of your python file}```. Now when you run the .exe, the console will not appear.

## Onefile
If you want all the files to be packed into one .exe you will need to add the 'F' flag. Thus the new statement will be ```pyinstaller -F {the name of your python file}```. Note that this will not work for all python scripts due to third party libraries or how the script works. You will find out if it works or not by running the .exe in the 'dist' folder.

## Adding an Icon
To add an icon to the final .exe (normal or onefile) add the 'i' flag and then the location of the .ico file (do not rename a .png/.jpg/.bmp to a .ico - I have had dumb people in the comments do this). You can find some nice icons [here](http://goo.gl/EfpGD0).

Thus the new statement will be ```pyinstaller -i {icon location} {python file}```, remember to not forget about extensions

## End Notes
You can combine these flags to make things like onefile executables with no console and an icon by using a statement like : ```pyinstaller -w -F -i {icon location} {python file}```

## Auto PY to EXE
In March 2018 I create a python package that allows you to create executables really easily from python scripts. It is built using a simple graphical interface built with Eel in Python.

{% include embedYouTube.html content="OZSZHmWSOeM" %}
![Empty interface](https://i.imgur.com/dd0LC2n.png)

## FAQ

### What is cmd?
A command prompt. This can alternatively be a terminal in Mac or Linux.

### Fatal error in launcher: Unable to create process using ' ''
Try ```python -m pip install pyinstaller``` in cmd

### 'pyinstaller' is not recognized as an internal or external command
Go back to the Pyinstaller heading, you have not set it up properly, remember to test it.

### Clicked the edit button and its only the variable name and value
Add a ';' to the end and then put in the folder location, then apply/save it.

*Please leave questions and comments related to the video on YouTube as they will be replied to faster there*
