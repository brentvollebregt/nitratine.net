---
templateKey: blog-post
title: "How to Use pynput's Mouse and Keyboard Listener at the Same Time"
date: 2020-05-18T12:00:00.000Z
category: Tutorials
tags: [pynput, python, mouse, keyboard]
image: feature.png
description: "In this tutorial I show you how to fix naming collisions from Python imports and provide an example of using pynput's mouse and keyboard listeners together."
hidden: false
---

[TOC]

## Background

In my posts like ["How To Get Mouse Clicks With Python"](/blog/post/how-to-get-mouse-clicks-with-python/) and ["How to Detect Key Presses In Python"](/blog/post/how-to-detect-key-presses-in-python/), I discuss how to use pynput to listen to mouse and keyboard events. 

When trying to use the two listeners at the same time, I see a lot of people copy and paste the two import statements like the following:

```python
from pynput.mouse import Listener
from pynput.keyboard import Listener
```

Looking at the code above, ask yourself, how do I create the mouse listener? If you follow the  example from [my tutorial](/blog/post/how-to-get-mouse-clicks-with-python/), you would use the following:
 
```python
with Listener(on_move=on_move, ...) as listener:
    listener.join()
```
 
However, when you run this, you will find that `Listener` is now `pynput.keyboard.Listener`, not `pynput.mouse.Listener`. This has occurred because the second import statement has overwritten `Listener`.

## Solution
Solutions to this are very simple and are not specific to pynput as this is just an import mistake. You can use these solutions for other related import naming collisions.

### Solution 1 - The "`as`" Keyword
The first solution I recommend is to use the Python `as` keyword. This keyword allows you to rename an imported object when importing. In the situation this post focuses on, you would do:

```python
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
```

This is very similar to the following:

```python
from pynput.mouse import Listener
MouseListener = Listener
from pynput.keyboard import Listener
KeyboardListener = Listener
```

So now when you want to use the two listeners, you would do:

```python
# Listen to mouse events
with MouseListener(...) as mouse_listener:
    mouse_listener.join()
    
# Listen to keyboard events
with KeyboardListener(...) as keyboard_listener:
    keyboard_listener.join()
```

> If you are to use the exact code above, remember these listener objects are threads, so when you call `.join()`, they will block.


### Solution 2 - Only Import the Base
Another solution which is a little more verbose in the usages is to just import the base library. To do this for our example, we would simply import `pynput`:

```python
import pynput
```

Then to use it like we have done above:

```python
# Listen to mouse events
with pynput.mouse.Listener(...) as mouse_listener:
    mouse_listener.join()
    
# Listen to keyboard events
with pynput.keyboard.Listener(...) as keyboard_listener:
    keyboard_listener.join()
```

## Mouse and Keyboard Listener Example

```python
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener


def on_press(key):
    print("Key pressed: {0}".format(key))

def on_release(key):
    print("Key released: {0}".format(key))

def on_move(x, y):
    print("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


# Setup the listener threads
keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

# Start the threads and join them so the script doesn't end early
keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()
```

> You can leave the `.join()` calls out if you provide some other method of stopping the application exit, like a while loop.
