title: "Python Auto Clicker"
date: 2018-02-09
category: YouTube
tags: [python, mouse, pynput]
feature: feature.jpg
description: "This is a script that allows you to click you mouse repeatedly with a small delay. It works on windows, mac and linux and can be controlled with user defined keys."

[TOC]

{% with video_id="eamTeszpeZ4" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}

## What is this?
This project uses the cross platform module pynput to control the mouse and monitor the keyboard at the same time to create a simple auto clicker.

## PIP
If you haven't used or setup pip before, look at my tutorial on [how to setup python's pip](/blog/post/how-to-setup-pythons-pip/) to setup pip.

## Installing Pynput
We will be using the punput module to listen to mouse events. To install this module execute ```pip install pynput``` in cmd. Watch the output to make sure no errors have occurred; it will tell you when the module has been successfully installed.

![Installing pynput](/post-assets/how-to-get-mouse-clicks-with-python/pynput1.png)

To double check that it was installed successfully, open up IDLE and execute the command ```import pynput```; no errors should occur.

![Testing pynput](/post-assets/how-to-get-mouse-clicks-with-python/pynput2.png).

## Writing the Code
First we need to import time and threading. Then import Button and Controller from pynput.mouse so we can control the mouse and import Listener and KeyCode from pynput.keyboard so we can watch for keyboard events to start and stop the auto clicker.

```python
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
```

Next create four variables as shown below. 'delay' will be the delay between each button click. 'button' will be the button to click, this can be either 'Button.left', 'Button.right' or even 'Button.middle'. 'start_stop_key' is the key you want to use to start and stop the auto clicker. I have set it to the key 's' to make it nice and simple, you can use any key here. Finally the 'exit_key' is the key to close the program set it like before, but make sure it is a different key.

```python
delay = 0.001
button = Button.left
start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')
```

No create a class that extends threading.Thread that will allow us to control the mouse clicks. Pass they delay and button to this and have two flags that determine whether it is running or if the whole program is stopping.

```python
class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True
```

Next add the methods shown below to control the thread externally.

```python
    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False
```

Now we need to create the method that is run when the thread starts. We need to keep looping while the program_running is true and then create another loop inside that checks if the running is set to true. If we are inside both loops, click the set button and then sleep for the set delay.

```python
    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)
```

Now we want to create an instance of the mouse controller, create a ClickMouse thread and start it to get into the loop in the run method.

```python
mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()
```

Now create a method called on_press that takes a key as an argument and setup the keyboard listener.

```python
def on_press(key):
    pass

with Listener(on_press=on_press) as listener:
    listener.join()
```

Now modify the on_press method. If they key pressed is the same as the start_stop_key, stop clicking if the running flag is set to true in the thread otherwise start it. If they key pressed is the exit key, call the exit method in the thread and stop the listener. The new method will look like this:

```python
def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()
```

This script can be saved as a .pyw to run in the background. It can easily be still closed using the set exit key even when no dialog is shown.

## Using the Script

To use this script set the variables at the top to what you want.
- delay: They delay between each mouse click
- button: The mouse button to click (Button.left&#124;Button.middle&#124;Button.right)
- start_stop_key: They key to start and stop clicking. Make sure this is either from the Key class or set using a KeyCode as shown.
- exit_key: The key to stop the program.Make sure this is either from the Key class or set using a KeyCode as shown.

Then run the script and use the start/stop key when wanted. Press the set exit key to exit.

## Final Code
```python
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode


delay = 0.001
button = Button.left
start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
```

## Common Issues and Questions

### ModuleNotFoundError/ImportError: No module named 'pynput'
Did you install pynput? This error will not occur if you installed it properly. If you have multiple versions of Python, make sure you are installing pynput on the same version as what you are running the script with.

### I got a SyntaxError
Syntax errors are caused by you and these is nothing I can offer to fix it apart from telling you to read the error. They always say where the error is in the output using a ^. Generally people that get this issue have incorrect indentation, brackets in the wrong place or something spelt wrong. You can read about SyntaxError on Python's docs [here](https://docs.python.org/2/tutorial/errors.html#syntax-errors).

### 'python' is not recognized as an internal or external command
Python hasn't been installed or it hasn't been installed properly. Go to [/blog/post/how-to-setup-pythons-pip/](/blog/post/how-to-setup-pythons-pip/) and follow the tutorial. Just before you enter the scripts folder into the path variable, remove the "\scripts\" part at the end. You will also want to add another path with "\scripts\" to have pip.

*Edited 11/08/18: Added Python 2 support*
