title: "How to Make Hotkeys in Python"
date: 2018-01-13
category: YouTube
tags: [python, keyboard, pynput]
feature: feature.jpg
description: "This demonstrates how to make a script to detect combinations of keypresses or even single keys pressed in Python. The script will use pynput to detect keypresses and will work on windows, mac and linux."

[TOC]

youtube:n_dfv5DLCGI

## PIP
If you haven't used or setup pip before, go to my tutorial at [how-to-setup-pythons-pip](/blog/post/how-to-setup-pythons-pip/) to setup pip.

## Installing Pynput
We will be using the pynput module to listen to mouse events. To install this module execute ```pip install pynput``` in cmd. Watch the output to make sure no errors have occurred; it will tell you when the module has been successfully installed.

![Installing pynput](/posts/how-to-get-mouse-clicks-with-python/pynput1.png)

To double-check that it was installed successfully, open up IDLE and execute the command ```import pynput```; no errors should occur.

![Testing pynput](/posts/how-to-get-mouse-clicks-with-python/pynput2.png)

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

Next we need to declare the combinations to look out for. I this example I will use [[Shift]] + [[A]]. I will need to use two variants, Shift + A and Shift + a so the combination will be detected no matter what order they are pressed. If [[A]] is pressed first, 'a' will be given to the listener but if [[Shift]] is pressed before [[A]] then 'A' will be given to the listener. Make a list called COMBINATIONS and add the keys in sets as shown below.

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

> In the current state, this script can provide multiple events for one combination detected. To prevent this, append ```and not key in current``` to the end of the initial if statement (before the colon).

Finally we need to modify the on_release method and check that when a key is released, if it is in any of the combinations. If it is we need to removed it from the 'current' set.

```python
def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
```

You can now run the script and when [[Shift]] and [[A]] are pressed at the same time, the sting will be printed to the console.

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

## Issues With Character Casing (Revision 1)
In the example above I have defined two combinations, one for [[Shift]] + [[A]] and [[Shift]] + [[A]]; this handles the two cases when you press [[A]] before [[Shift]] and [[Shift]] before [[A]]. However this mixing of case can also cause issues when tracking the currently pressed keys.

A better way would be to track what physical key is pressed, rather than what the actual value of it is. An example of this is that pressing the [[A]] key can give two different keys depending on if you are holding [[Shift]] or not (a or A); but pynput can actually see that the [[A]] key itself is pressed. To track what physical key is pressed, we can use the `vk`. 

> `vk` is short for "virtual key" and is a code associated with each key. For example: a = 65, b = 66, enter = 13, shift = 130

To get the vk, we can read the `vk` attribute in the `KeyCode` object provided by pynput in the `on_press` and `on_release`. Using the `vk` codes to track what keys are pressed will take a bit more effort but can simplify some things.

Below is a script I developed to watch for [[Shift]] + [[A]]. This will now be able to handle [[Shift]] + [[A]] pressed in many different ways.

```python
from pynput import keyboard

# The key combinations to look for
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(vk=65)}  # shift + a (see below how to get vks)
]


def execute():
    """ My function to execute when a combination is pressed """
    print("Do Something")


# The currently pressed keys (initially empty)
pressed_vks = set()


def get_vk(key):
    """
    Get the virtual key code from a key.
    These are used so case/shift modifications are ignored.
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination):
    """ Check if a combination is satisfied using the keys pressed in pressed_vks """
    return all([get_vk(key) in pressed_vks for key in combination])


def on_press(key):
    """ When a key is pressed """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.add(vk)  # Add it to the set of currently pressed keys

    for combination in COMBINATIONS:  # Loop though each combination
        if is_combination_pressed(combination):  # And check if all keys are pressed
            execute()  # If they are all pressed, call your function
            break  # Don't allow execute to be called more than once per key press


def on_release(key):
    """ When a key is released """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()  # Join the listener thread to the current thread so we don't exit before it stops
```

At the top of this script you will see that the `COMBINATIONS` value looks a bit different. This is because `keyboard.KeyCode(char='a')` does not populate the `vk` attribute, so we need to find the `vk` code ourselves. 

Doing this can easily be done using a simple script. If you run the following and press a key, it will print out the `vk` code for the pressed key which you can then use in the script above.

```python
from pynput import keyboard

def on_press(key):
    vk = key.vk if hasattr(key, 'vk') else key.value.vk
    print('vk =', vk)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
```

If you pressed shift, you would have also noticed that the `vk` for `keyboard.Key.shift` is 160. Instead of using `keyboard.Key.shift` in the `COMBINATIONS`, this shows you could also use `keyboard.KeyCode(vk=160)`. The reason we could leave the shift key as `keyboard.Key.shift` in `COMBINATIONS` is because pynput is able to populate the `vk` value in the key object.

Here are some other `vk` codes, you can find missing ones by running the script above and pressing keys:

| Key        | vk code |
|------------|---------|
| a          | 65      |
| b          | 66      |
| y          | 89      |
| z          | 90      |
| Top row 1  | 49      |
| Num pad 1  | 97      |
| Insert     | 45      |
| Enter      | 13      |
| Left ctrl  | 162     |
| Right ctrl | 163     |

> An interesting thing to note from this table is that you can tell the difference between 1 in the top row being pressed and 1 on the num pad being pressed.

## An Improved Script
A lot of people had been asking for a solution that can handle different functions for different combinations. [Christopher Walters](https://www.youtube.com/channel/UCzGG-Z4QAgkt2uYMH6VTpQQ) commented on the original video with a snippet that allowed users to declare a function per combination.

I modified the original script and after revisions made to the original script, here is a script that can handle multiple combinations that execute their own function:

```python
from pynput.keyboard import Key, KeyCode, Listener


def function_1():
    """ One of your functions to be executed by a combination """
    print('Executed function_1')


def function_2():
    """ Another one of your functions to be executed by a combination """
    print('Executed function_2')


# Create a mapping of keys to function (use frozenset as sets/lists are not hashable - so they can't be used as keys)
# Note the missing `()` after function_1 and function_2 as want to pass the function, not the return value of the function
combination_to_function = {
    frozenset([Key.shift, KeyCode(vk=65)]): function_1,  # shift + a
    frozenset([Key.shift, KeyCode(vk=66)]): function_2,  # shift + b
    frozenset([Key.alt_l, KeyCode(vk=71)]): function_2,  # left alt + g
}


# The currently pressed keys (initially empty)
pressed_vks = set()


def get_vk(key):
    """
    Get the virtual key code from a key.
    These are used so case/shift modifications are ignored.
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination):
    """ Check if a combination is satisfied using the keys pressed in pressed_vks """
    return all([get_vk(key) in pressed_vks for key in combination])


def on_press(key):
    """ When a key is pressed """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.add(vk)  # Add it to the set of currently pressed keys

    for combination in combination_to_function:  # Loop through each combination
        if is_combination_pressed(combination):  # Check if all keys in the combination are pressed
            combination_to_function[combination]()  # If so, execute the function


def on_release(key):
    """ When a key is released """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
```

When executing this script and pressing [[Shift]] + [[A]] (in any order), this will execute `function_1` and print "Executed function_1". When pressing [[Shift]] + [[B]] (in any order), `function_2` will be executed. Also when pressing Left [[alt]] + [[G]] (in any order), `function_2` will be executed.

To create new combinations, duplicate a line in the `combination_to_function` dictionary and replace the keys inside of `frozenset` and the value (function - not the return value of the function).

## pynput's HotKey Class
In December 2019 [global hotkeys](https://pynput.readthedocs.io/en/latest/keyboard.html#global-hotkeys) were added to pynput. This allowed us to hide all the extra state of combination detection and just provide the keys we want to listen to.

The docs recommend using `keyboard.HotKey.parse` to get a list of keys from a string (e.g. `"<ctrl>+<alt>+h"`) when using this function, but I recommend using keys like we defined above. This allows you to more easily identify keys are pynput keys although there aren't huge benefits using either way.

Here is an example of [[Alt]] + [[Ctrl]] + [[R]]:

```python
from pynput.keyboard import HotKey, Key, KeyCode, Listener


# The function called when a hotkey is pressed
def on_activate():
    print('Hotkey pressed')


# A helper function when delegating on_press/on_release events
def for_canonical(f):
    return lambda k: f(l.canonical(k))


# The hotkey itself
hotkey = HotKey(
    [Key.alt, Key.ctrl, KeyCode(char='r')],  # A list of the keys to look for
    on_activate  # The function to call when a hotkey is pressed
)

# The typical pynput listener that is calling functions on hotkey using `for_canonical`
with Listener(
    on_press=for_canonical(hotkey.press),
    on_release=for_canonical(hotkey.release)
) as l:
    l.join()
```

An example of more than one hotkey would be something like:

```python
from pynput.keyboard import HotKey, Key, KeyCode, Listener


def function_1():
    print('Function 1 activated')

def function_2():
    print('Function 2 activated')


hotkey1 = HotKey(
    [Key.alt, Key.ctrl, KeyCode(char='r')],
    function_1
)

hotkey2 = HotKey(
    [Key.alt, Key.ctrl, KeyCode(char='t')],
    function_1
)

hotkey3 = HotKey(
    [Key.alt, Key.ctrl, KeyCode(char='y')],
    function_2
)

hotkeys = [hotkey1, hotkey2, hotkey3]


def signal_press_to_hotkeys(key):
    for hotkey in hotkeys:
        hotkey.press(l.canonical(key))

def signal_release_to_hotkeys(key):
    for hotkey in hotkeys:
        hotkey.release(l.canonical(key))

with Listener(on_press=signal_press_to_hotkeys, on_release=signal_release_to_hotkeys) as l:
    l.join()
```

However using `keyboard.HotKey.parse` would make things a lot easier for that example:

```python
from pynput import keyboard

def function_1():
    print('Function 1 activated')

def function_2():
    print('Function 2 activated')

with keyboard.GlobalHotKeys({
        '<alt>+<ctrl>+r': function_1,
        '<alt>+<ctrl>+t': function_1,
        '<alt>+<ctrl>+y': function_2}) as h:
    h.join()
```

> In this example, `keyboard.HotKey.parse` is being used in the background by keyboard.GlobalHotKeys.

## Common Issues and Questions

### ModuleNotFoundError/ImportError: No module named 'pynput'
Did you install pynput? This error will not occur if you installed it properly. If you have multiple versions of Python, make sure you are installing pynput on the same version as what you are running the script with.

### I got a SyntaxError
Syntax errors are caused by you and these is nothing I can offer to fix it apart from telling you to read the error. They always say where the error is in the output using a ^. Generally people that get this issue have incorrect indentation, brackets in the wrong place or something spelt wrong. You can read about SyntaxError on Python's docs [here](https://docs.python.org/2/tutorial/errors.html#syntax-errors).
