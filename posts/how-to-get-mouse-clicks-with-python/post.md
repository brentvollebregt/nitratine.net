title: "How To Get Mouse Clicks With Python"
date: 2017-12-14
category: YouTube
tags: [python, mouse, logging, pynput]
feature: demo2.png
description: "This demonstration shows you how to track mouse clicks, movements and even scrolls using the pynput module. These can then be logged to a file as no console is displayed. This is very similar to a mouse logger."

[TOC]

{% with video_id="kJshtCfqCsY" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}

## PIP
If you haven't used or setup pip before, go to my tutorial at [how-to-setup-pythons-pip]({{ url_for('blog_post', path='how-to-setup-pythons-pip') }}) to setup pip.

## Installing Pynput
We will be using the pynput module to listen to mouse events. To install this module execute ```pip install pynput``` in cmd. Watch the output to make sure no errors have occurred; it will tell you when the module has been successfully installed.

![Installing pynput](/posts/how-to-get-mouse-clicks-with-python/pynput1.png)

To double check that it was installed successfully, open up IDLE and execute the command ```import pynput```; no errors should occur.

![Testing pynput](/posts/how-to-get-mouse-clicks-with-python/pynput2.png)

## Building the Script
Create a new python file and save it with a .py file extension. You will first want to import Listener from pynput.mouse.

```python
from pynput.mouse import Listener
```

Setup the listener by creating an instance in a with statement and using it's .join() method to join it to the main thread.

```python
with Listener() as listener:
    listener.join()
```

Create three methods; on_move, on_click and on_scroll with the parameters as shown below.

```python
def on_move(x, y):
    pass

def on_click(x, y, button, pressed):
    pass

def on_scroll(x, y, dx, dy):
    pass
```

Link these methods to the listener instance with the function names as the args; I have named the methods as the are defined in the listener class. Now when an action occurs, one of these methods will be run.

```python
with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
```

To make sure these are running, add some print statements to each method. Save and run the script. Move your mouse around a bit, you should see output as below.

```python
def on_move(x, y):
    print ("Mouse moved")

def on_click(x, y, button, pressed):
    print ("Mouse clicked")

def on_scroll(x, y, dx, dy):
    print ("Mouse scrolled")
```

![Mouse moved demonstration](/posts/how-to-get-mouse-clicks-with-python/demo1.png)

Using these print statements and the parameters provided, we can give more information when a print. Run this again to make sure it is working properly (example output below).

```python
def on_move(x, y):
    print ("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        print ('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    print ('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
```

![Mouse moved demonstration with data](/posts/how-to-get-mouse-clicks-with-python/demo2.png)

If you want this script to be run in the background. Click File -> Save As and save it with a .pyw file extension. Now when it is run outside IDLE there will be no console window and it will not look like it is running. But to make sure the console doesn't appear, we need to first remove the print statements.

Import logging and setup the basic configuration as I have below. After that, change all print statements to logging.info.

```python
import logging
```

```python
logging.basicConfig(filename=("mouse_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
```

```python
def on_move(x, y):
    logging.info("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
```

Now when the script is run, nothing should be printed to the console. This is because it is all being saved to the file declared in the basic configuration.

Save and close IDLE. Open the file named mouse_log.txt next to your python script; all the events should be logged in here.

## The Listener Thread
Just as a quick note, the Listener class is a thread which means as soon as it has joined to the main thread no code will be executed after the .join() until the Listener is stopped.

As stated [here in the pynput docs on readthedocs.io](https://pynput.readthedocs.io/en/latest/mouse.html#controlling-the-mouse), we can call pynput.mouse.Listener.stop anywhere in the script to stop the thread or return False from a callback to stop the listener. As shown in my video, we can also just call listener.stop() in one of the definitions due to the fact that that the listener is now in scope and is an instance os Listener.

## Final Script
```python
from pynput.mouse import Listener
import logging

logging.basicConfig(filename=("mouse_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_move(x, y):
    logging.info("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
```

## Common Issues and Questions

### ModuleNotFoundError/ImportError: No module named 'pynput'
Did you install pynput? This error will not occur if you installed it properly. If you have multiple versions of Python, make sure you are installing pynput on the same version as what you are running the script with.

### I got a SyntaxError
Syntax errors are caused by you and these is nothing I can offer to fix it apart from telling you to read the error. They always say where the error is in the output using a ^. Generally people that get this issue have incorrect indentation, brackets in the wrong place or something spelt wrong. You can read about SyntaxError on Python's docs [here](https://docs.python.org/2/tutorial/errors.html#syntax-errors).
