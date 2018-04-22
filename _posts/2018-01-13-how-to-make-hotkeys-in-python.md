---
layout: post
title: "How to Make Hotkeys in Python"
date: 2018-01-13
categories: Youtube
tags: Python Keyboard pynput
---

* content
{:toc}

This demonstrates how to make a script to detect combinations of keypresses or even single keys pressed in Python. The script will use pynput to detect keypresses and will work on windows, mac and linux.

{% include embedYouTube.html content="n_dfv5DLCGI" %}

<!-- more -->

## PIP
If you haven't used or setup pip before, go to my tutorial at [{% link _posts/2017-12-13-how-to-setup-python's-pip.md %}]({{ site.baseurl }}{% link _posts/2017-12-13-how-to-setup-python's-pip.md %}) to setup pip.

## Installing Pynput
We will be using the punput module to listen to mouse events. To install this module execute ```pip install pynput``` in cmd. Watch the output to make sure no errors have occurred; it will tell you when the module has been successfully installed.

![Installing pynput](/images/how-to-get-mouse-clicks-with-python-pynput1.png)

To double check that it was installed successfully, open up IDLE and execute the command ```import pynput```; no errors should occur.

![Testing pynput](/images/how-to-get-mouse-clicks-with-python-pynput2.png)

## Creating the Script
First import keyboard from pynput and create a variable called current and set it to a set object to track what keys are pressed currently.

```python
from pynput import keyboard

# The currently active modifiers
current = set()
```

Next we will setup a listener for the keyboard and set on press and release methods to it. Setup the listener in a with statement and join the listener thread to the main thread using .join().

```python
def on_press(key):
    pass

def on_release(key):
    pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
```

Next we need to the the combinations to look out for. I this example I will use Shift + A. I will need to use two variants, Shift + A and Shift + a so the combination will be detected no matter what order they are pressed. If A is pressed first, 'a' will be given to the listener but if shift is pressed before A then 'A' will be given to the listener. Make a list called COMBINATIONS and add the keys in sets as shown below.

```python
# The key combination to check
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='a')},
    {keyboard.Key.shift, keyboard.KeyCode(char='A')}
]
```

Now create a method called execute. This is what will be executed when a combination is detected. You can put anything in here but for the demonstration I will print a simple string.

```python
def execute():
    print ("Do Something")
```

Now we will edit the on_press method. We need to first check if the key that has just been pressed is in any of the combinations that we have. If it is we need to add it to the current key set and then loop though all the combinations checking if all the keys in a particular combination are in the 'current' set. If one of the combinations has all their keys down, we need to call execute().

```python
def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()
```

> In the current state, this script can provide multiple events for one combination detected. To prevent this, append " and not key in current" to the end of the initial if statement (before the colon).

Finally we need to modify the on_release method and check that when a key is released, if it is in any of the combinations. If it is we need to removed it from the 'current' set.

```python
def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
```

You can now run the script and when Shift and 'A' are pressed at the same time, the sting will be printed to the console.

If you want to call another script, do it in execute() by doing something like an os.system call on your script or importing it and then calling it.

This script has been modified from the example given by Moses Palmer on [issue 20 of pynput](https://github.com/moses-palmer/pynput/issues/20)

## Adding Hotkeys
To add more hotkeys or different hotkeys you will need to add another set of keys to the COMBINATIONS list. To do this use curly braces and make sure to separate the keys by commas. Also to make sure to split each set by a comma or you will be given an error when running the script.

To use keys like shift and control, you need to provide the key. Keys can be found in the [documentation](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key). In this we can see that if we want to use shift, we need to use keyboard.Key.shift. Another example is the scroll lock: keyboard.Key.scroll_lock. To use characters on the keyboard like 'a', 'b', 'c' ect... you will need to use the method keyboard.KeyCode() passing the character as the char parameter. Examples follow below.

```python
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='a')}, # Shift + a
    {keyboard.Key.shift, keyboard.KeyCode(char='A')}, # Shift + A
    {keyboard.Key.scroll_lock}, # Scroll lock
    {keyboard.KeyCode(char='q')}, # q
    {keyboard.KeyCode(char='Q')}, # Q
    {keyboard.Key.shift, keyboard.Key.insert, keyboard.Key.ctrl} # Shift + Insert + Ctrl
]
```

You can have as many keys as you like in one combination and accidentally adding two of the same combination will not cause any errors.

## Final Script
```python
from pynput import keyboard

# The key combination to check
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='a')},
    {keyboard.Key.shift, keyboard.KeyCode(char='A')}
]

# The currently active modifiers
current = set()

def execute():
    print ("Do Something")

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
```

*Please leave questions and comments related to the video on YouTube as they will be replied to faster there*
