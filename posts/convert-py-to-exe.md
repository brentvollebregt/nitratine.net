title: "Convert .py to .exe"
date: 2017-12-11
categories: YouTube
tags: [Python, pyinstaller]
feature: demo6.png
description: "A demonstration of how to package a python script into an executable file. This tutorial includes compiling to one file, no console, how to add an icon and adding other files to the final package."

[TOC]

{% with video_id="lOIJIk_maO4" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}

## PIP
If you haven't used or setup pip before, go to my tutorial at [how-to-setup-pythons-pip]({{ url_for('blog_post', path='how-to-setup-pythons-pip') }}) to setup pip.

## PyInstaller
Now that pip has been setup, execute the command ```pip install pyinstaller``` in cmd. Make sure to check the output for errors as if there are errors it would not have installed successfully. PyInstaller now supports Python 2.7 - 3.7 including Python 3.7.

To make sure it installed properly, type ```pyinstaller``` in cmd and make sure no errors appeared.

![pyinstaller command output](/post-assets/convert-py-to-exe/demo6.png)
## Basic Compiling
Created a new folder and put your python file in it and any other modules or files it may need. Then hold shift and right click in the folder, in the menu that popped up, click "Open PowerShell Window Here" or "Open command window here" for older versions of windows. If this option doesn't appear, try again or open cmd and type ```cd {folder location}``` to move to that folder.

![Open PowerShell window here](/post-assets/convert-py-to-exe/demo7.png)

Now that cmd is in the right location, execute ```pyinstaller {the name of your python file}``` make sure to add .py or whatever extension it has. Wait for it to finish and check if any errors have appeared. If none have you can close cmd and look at the three folders generated.

Look in the 'dist' folder and you should see {the name of your script}.exe. If you run that your script should execute as an exe.

## No Console
When running the compiled script, you will notice a console window will appear. If you do not want this, add the 'w' flag to the statement when creating the script.

Thus the new statement will be ```pyinstaller -w {the name of your python file}```. Now when you run the .exe, the console will not appear.

## Onefile
If you want all the files to be packed into one .exe you will need to add the 'F' flag. Thus the new statement will be ```pyinstaller -F {the name of your python file}```. Note that this will not work for all python scripts due to third party libraries or how the script works. You will find out if it works or not by running the .exe in the 'dist' folder.

> If you want to use onefile mode with external files, it will pay to read [this](https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741)

## Adding an Icon
To add an icon to the final .exe (normal or onefile) add the 'i' flag and then the location of the .ico file (do not rename a .png/.jpg/.bmp to a .ico - I have had dumb people in the comments do this). You can find some nice icons [here](http://goo.gl/EfpGD0).

Thus the new statement will be ```pyinstaller -i {icon location} {python file}```, remember to not forget about extensions

## End Notes
You can combine these flags to make things like onefile executables with no console and an icon by using a statement like : ```pyinstaller -w -F -i {icon location} {python file}```

## Auto PY to EXE
In March 2018 I create a python package that allows you to create executables really easily from python scripts. It is built using a simple graphical interface built with Eel in Python.

{% with video_id="OZSZHmWSOeM" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}

![Empty interface](https://i.imgur.com/dd0LC2n.png)

## Common Issues and Questions

### My script runs fine in IDLE but won't run when packaged to exe
Regarding that the python script runs properly by itself then this would have been caused by incorrect configuration or third party modules. The best way to find what the issue is, is to add the -d flag and then re-package it. This will mean the exe is now in a debugging mode. Open up cmd and then run the exe using cmd e.g. "C:/folder/path/myexe.exe". Any errors will be preserved in the console which you were previously missing.

### zipimport.ZipImportError: can't find module 'encodings'﻿
Please upgrade PyInstaller to 3.4 or above using: `python -m pip install --upgrade PyInstaller`

### "Open command window here" isn't shown when I shift right click?
Make sure you are holding down shift. If you are using new versions of Windows, this has been replaced by "Open PowerShell Window Here". Using this method will work exactly the same for this tutorial; so go ahead and use PowerShell.

### 'pip' is not recognized as an internal or external command
Please follow the pip setup again, you have done something wrong. Alternatively, you can try to use `python -m pip {command}`.

### Fatal error in launcher: Unable to create process using...
Try executing ```python -m pip install pyinstaller``` in cmd.

### 'pyinstaller' is not recognized as an internal or external command
Go back to the PyInstaller heading, you have not installed pyinstaller, remember to test it.

### When editing the PATH variable, I can only edit the variable
Add a ';' to the end and then put in the folder location, then apply/save it. This input is like this because you are using an older version of Windows.

### The exe does not work on another computer﻿
This may be an architecture issue. PyInstaller will create an executable with the architecture of the machine it was built with. You are most likely using a 64bit machine if you are asking this question to compile the .py; thus it will create a 64bit executable. As with any other programs, you cannot run 64bit on 32bit but you can run 32bit on 64bit. Thus I recommend using 32bit python or compiling on a 32bit machine so it will work on both architectures﻿.

### My antivirus detected my exe as a virus
This is your anti-virus vendors fault. Check out [this](https://github.com/pyinstaller/pyinstaller/issues/2501#issuecomment-286230354).

### I get lots of WARNINGs when running pyinstaller
These warnings can be ignored in most cases. I have not currently found a situation where these are an issue, after-all, they are only warnings.

### Will this add my other scripts? / Will this work with external Python modules?﻿
Regarding that your main script imports your others scripts, then yes. PyInstaller looks at imports to figure out what to bundle, so it will add your other scripts just like if you were to import os or time.

### [is it available in Walmart?????﻿](https://www.youtube.com/watch?v=lOIJIk_maO4&lc=UgxFJKkC5nzr7MiscOd4AaABAg)
I don't believe so, sorry.
