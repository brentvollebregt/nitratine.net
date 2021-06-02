title: "Simulate Mouse Events In Python"
date: 2018-01-13
category: YouTube
tags: [python, mouse, pynput]
feature: feature.jpg
description: "This demonstrates how to control the mouse with Python. Using pynput we are able to simulate mouse events into any window. This will show you how to press buttons, scroll and move the mouse."

[TOC]

youtube:2BXr9U6ZL8Y

## PIP
If you haven't used or setup pip before, go to my tutorial at [how-to-setup-pythons-pip](/blog/post/how-to-setup-pythons-pip/) to setup pip.

## Installing Pynput
We will be using the pynput module to listen to mouse events. To install this module execute ```pip install pynput``` in cmd. Watch the output to make sure no errors have occurred; it will tell you when the module has been successfully installed.

![Installing pynput](/posts/how-to-get-mouse-clicks-with-python/pynput1.png)

To double-check that it was installed successfully, open up IDLE and execute the command ```import pynput```; no errors should occur.

![Testing pynput](/posts/how-to-get-mouse-clicks-with-python/pynput2.png)

## Simulating Mouse Events
Create a new script and save it somewhere so you can easily run the script. Import `Button` and `Controller` from `pynput.mouse`.

```python
from pynput.mouse import Button, Controller
```

Make a variable called `mouse` and set it to an instance of `Controller`. Now using the `mouse` variable we can control the mouse.

```python
mouse = Controller()
```

### Finding the Position of the Mouse
To find the position of the mouse we can use `mouse.position`. This will return a tuple of two integers. The first integer is the x position and the second integer is the y position. This is relative to the top left of the screen; x getting bigger is going right and y getting bigger is going down.

```python
print ("Current position: " + str(mouse.position))
```

### Setting the Position of the Mouse
To set the position of the mouse we can use `mouse.position` again. By setting this to an x and y point, the mouse position will be updated immediately.

```python
mouse.position = (10, 20)
```

### Moving the Mouse Relative to Its Position
Instead of getting the mouses position and calculating where it needs to be moved to, if you want to move it a distance relative to the current position, we can use `mouse.move`. Passing an x and y integers to this will move the mouse relative to its current position. For example, if I wanted to move it to the right by 20 pixels and up by 13 pixels, I would use:

```python
mouse.move(20, -13)
```

### Clicking Buttons on the Mouse
To click buttons on the mouse, we would use `mouse.click`. Passing a button from the Button class imported and an integer, we can perform single, double and triple clicks for any button.

```python
# Click the left button
mouse.click(Button.left, 1)
# Click the right button
mouse.click(Button.right, 1)
# Click the middle button
mouse.click(Button.middle, 1)
# Double click the left button
mouse.click(Button.left, 2)
# Click the left button ten times
mouse.click(Button.left, 10)
```

### Pressing and Releasing Buttons
We can also click a button using press and release methods. This would also allow us to drag an object by pressing, moving and then releasing. To press we would use the mouse.press method and to release we would use the `mouse.release` method. Both these methods need a button passed which can include the left, middle and right as shown above. More buttons can also be included depending on what operating system is being used.

```python
mouse.press(Button.left)
mouse.release(Button.left)
```

### Scrolling
To scroll we need to use the `mouse.scroll` passing two integers for horizontal and vertical scroll. The first integer is for horizontal which is left to right scroll; a positive integer will scroll right vice versa. The second integer is for vertical which is up to down scroll; a positive integer will scroll up vice versa.

```python
# Scroll up two steps
mouse.scroll(0, 2)
# Scroll right five steps
mouse.scroll(5, 0)
```

Depending on your mouse settings, you may need to use bigger step values to see movement in the scroll. I have witnessed this myself and sometimes may need to use around 100 steps to move my mouse.

## Common Issues and Questions

### How can I use the keyboard and mouse controllers at the same time?
When you import the classes, Controller will be set to the last one imported. To show what the issue was, ask yourself, what controller did you use to set the mouse and what one to set the keyboard? You would have used the same, but they need to be from the different classes.  So then you should use:
```python
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
```

Now when you want to use the controller for the mouse use MouseController and KeyboardController for the keyboard.
```
keyboard = KeyboardController()
mouse = MouseController()
```

### How can I simulate buttons other than right and left?
To simulate the other buttons on your mouse, you first need to identify them. An easy way to do this would be to write a quick script to identify the buttons when you press them:

```python
from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print('Pressed {0}'.format(button))

with Listener(on_click=on_click) as listener:
    listener.join()
```

This script creates a mouse listener and prints out the name of any button you press. To use this, run the script and press the target button on your mouse. You should see some output like this:

```text
Pressed Button.left
Pressed Button.x1
Pressed Button.x2
```

In this output above, you can see that I pressed the left button on my mouse and then two other buttons on my mouse (my forward and back buttons). Using the buttons you have now identified, you can use them, for example, `mouse.click(Button.x1)`.

### ModuleNotFoundError/ImportError: No module named 'pynput'
Did you install pynput? This error will not occur if you installed it properly. If you have multiple versions of Python, make sure you are installing pynput on the same version as what you are running the script with.

### I got a SyntaxError
Syntax errors are caused by you and there is nothing I can offer to fix it apart from telling you to read the error. They always say where the error is in the output using a ^. Generally, people that get this issue have incorrect indentation, brackets in the wrong place or something spelt wrong. You can read about SyntaxError on Python's docs [here](https://docs.python.org/2/tutorial/errors.html#syntax-errors).
