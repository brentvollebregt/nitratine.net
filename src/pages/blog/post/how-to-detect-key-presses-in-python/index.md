---
templateKey: blog-post
title: "How to Detect Key Presses In Python"
date: 2020-04-07T12:00:00.000Z
category: Tutorials
tags: [python, keyboard, logging, pynput]
image: demo2.png
description: "This demonstration shows you how to detect key presses using the pynput module. These can then be logged to a file as no console is displayed. This is very similar to a key logger."
disableToc: false
hidden: false
---

## PIP
If you haven't used or setup pip before, go to my tutorial at [how-to-setup-pythons-pip]({{ url_for('blog_post', path='how-to-setup-pythons-pip') }}) to setup pip.

## Installing Pynput
We will be using the pynput module to listen to keyboard events. To install this module execute ```pip install pynput``` in cmd. Watch the output to make sure no errors have occurred; it will tell you when the module has been successfully installed.

![Installing pynput](../how-to-get-mouse-clicks-with-python/pynput1.png)

To double-check that it was installed successfully, open up IDLE and execute the command ```import pynput```; no errors should occur.

![Testing pynput](../how-to-get-mouse-clicks-with-python/pynput2.png)

## Building the Script
Create a new python file and save it with a .py file extension. You will first want to import Listener from pynput.keyboard.

```python
from pynput.keyboard import Listener
```

Setup the listener by creating an instance in a `with` statement and using it's `.join()` method to join it to the main thread.

```python
with Listener() as listener:
    listener.join()
```

Create three methods; on_press and on_release with the parameters as shown below.

```python
def on_press(key):
    pass

def on_release(key):
    pass
```

Link these methods to the listener instance with the function names as the args; I have named the methods as they are defined in the listener class. Now when an action occurs, one of these methods will be run.

```python
with Listener(on_press=on_press, on_release=on_release) as listener:
```

To make sure these are running, add some print statements to each method. Save and run the script. Press a few keys, you should see output like below.

```python
def on_press(key):
    print("Key pressed")

def on_release(key):
    print("Key released")
```

![Keys pressed demonstration](demo1.png)

Using these print statements and the parameters provided, we can give more information when printing. Run this again to make sure it is working properly (example output below).

```python
def on_press(key):
    print("Key pressed: {0}".format(key))

def on_release(key):
    print("Key released: {0}".format(key))
```

![Keys pressed demonstration with data](demo2.png)

If you want this script to be run in the background. Click File -> Save As and save it with a .pyw file extension. Now when it is run outside IDLE there will be no console window and it will not look like it is running. But to make sure the console doesn't appear, we need to first remove the print statements.

Import logging and set up the basic configuration as I have below. After that, change all print statements to logging.info.

```python
import logging
```

```python
logging.basicConfig(filename="key_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')
```

```python
def on_press(key):
    logging.info("Key pressed: {0}".format(key))

def on_release(key):
    logging.info("Key released: {0}".format(key))
```

Now when the script is run, nothing should be printed to the console. This is because it is all being saved to the file declared in the basic configuration.

Save and close IDLE. Open the file named key_log.txt next to your python script; all the events should be logged in here. For example, here is one of my logs typing `Wow!`:

```text
2020-04-07 22:52:58,233: Key pressed: Key.shift
2020-04-07 22:52:58,514: Key pressed: 'W'
2020-04-07 22:52:58,649: Key released: Key.shift
2020-04-07 22:52:58,649: Key released: 'w'
2020-04-07 22:52:58,942: Key pressed: 'o'
2020-04-07 22:52:59,058: Key released: 'o'
2020-04-07 22:52:59,205: Key pressed: 'w'
2020-04-07 22:52:59,318: Key released: 'w'
2020-04-07 22:52:59,430: Key pressed: Key.shift
2020-04-07 22:52:59,590: Key pressed: '!'
2020-04-07 22:52:59,710: Key released: '!'
2020-04-07 22:52:59,853: Key released: Key.shift
```

> The actual location of this file will be in the current working directory of where you run the script from

## The Listener Thread
Just as a quick note, the Listener class is a thread which means as soon as it has joined to the main thread no code will be executed after the `.join()` until the Listener is stopped.

As stated [here in the pynput docs on readthedocs.io](https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard), we can call `pynput.keyboard.Listener.stop` anywhere in the script to stop the thread or return False from a callback to stop the listener. As shown in my video, we can also just call `listener.stop()` in one of the definitions due to the fact that that the listener is now in scope and is an instance os Listener.

## Final Script

```python
from pynput.keyboard import Listener
import logging

# Setup logging
logging.basicConfig(filename="key_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):  # The function that's called when a key is pressed
    logging.info("Key pressed: {0}".format(key))

def on_release(key):  # The function that's called when a key is released
    logging.info("Key released: {0}".format(key))

with Listener(on_press=on_press, on_release=on_release) as listener:  # Create an instance of Listener
    listener.join()  # Join the listener thread to the main thread to keep waiting for keys
```

## Making Things a Bit More Readable
Everything being on a new line with both key presses and releases can be very helpful for identifying sequences but can be a bit hard to read. Here is a modified script that can put everything on one line and enters when enter is pressed.

```python
from pynput.keyboard import Listener, Key

filename = "key_log.txt"  # The file to write characters to


def on_press(key):
    f = open(filename, 'a')  # Open the file

    if hasattr(key, 'char'):  # Write the character pressed if available
        f.write(key.char)
    elif key == Key.space:  # If space was pressed, write a space
        f.write(' ')
    elif key == Key.enter:  # If enter was pressed, write a new line
        f.write('\n')
    elif key == Key.tab:  # If tab was pressed, write a tab
        f.write('\t')
    else:  # If anything else was pressed, write [<key_name>]
        f.write('[' + key.name + ']')

    f.close()  # Close the file


with Listener(on_press=on_press) as listener:  # Setup the listener
    listener.join()  # Join the thread to the main thread
```

Here is a sample of some of the output:

```text
[shift]I am typing this in notepad
[shift]Here is a new line
[shift]Opps, [shift]I spelt that wro[backspace][backspace]ro[backspace][backspace]ord incorrectly
[shift]Here as [backspace][backspace]re some special keys[shift]:[shift][ctrl_l][alt_l][alt_r][ctrl_r][shift_r]
```

## Common Issues and Questions

### ModuleNotFoundError/ImportError: No module named 'pynput'
Did you install pynput? This error will not occur if you installed it properly. If you have multiple versions of Python, make sure you are installing pynput on the same version as what you are running the script with.

