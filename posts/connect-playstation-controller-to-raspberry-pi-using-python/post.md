title: "Connect PlayStation Controller to Raspberry Pi using Python"
date: 2024-10-05
category: Tutorials
tags: [python, raspberry-pi]
feature: feature.jpg
description: "We'll look at how to connect a PlayStation Controller to Raspberry Pi using Bluetooth and then receive controller events in Python using pyPS4Controller"

[TOC]

## Hardware

For this tutorial, I will be using a PlayStation 4 (PS4) Controller and a Raspberry Pi 5. I have tested this on a Raspberry Pi 4 also and that had no issues. This should also work for PlayStation 5 Controllers as they can connect with Bluetooth.

## Connecting the PlayStation Controller to the Raspberry Pi Using Bluetooth

The first step is to connect the controller to the Raspberry Pi.

On your Raspberry Pi, start Bluetooth scanning by doing the following:

1. Execute `bluetoothctl` in a terminal to open an interactive tool for controlling Bluetooth
   - Do not exit this yet
2. Execute `scan on` to start scanning

Now turn your PS4 controller on by holding down the PlayStation button and the share button at the same time until the light at the top of the controller starts flashing light blue.

After the light starts flashing, you should see your device show up in the interactive Bluetooth session with a name like "Wireless Controller". Execute `devices` to see all devices that has been found by the Raspberry Pi. You should see your device as something like "10:18:49:88:10:DE Wireless Controller" - this gives you the MAC address.

Now that you have the MAC address (10:18:49:88:10:DE in the example above), we can pair and connect:

1. Execute `pair [MAC_ADDRESS]` (e.g. `pair 10:18:49:88:10:DE`)
2. Execute `connect [MAC_ADDRESS]` (e.g. `connect 10:18:49:88:10:DE`)
3. Execute `trust [MAC_ADDRESS]` (e.g. `trust 10:18:49:88:10:DE`)

After executing step two above, you should have noticed that the light at the top of the controller has stopped flashing and is now solid blue - this means it's connected.

If it is not solid blue, you may have connected to something else!

You can type `exit` to leave `bluetoothctl` now.

## Identifying the Device

When the controller connects, a new file is created in `/dev/input` - typically it is `/dev/input/js0`.

In a terminal, execute `ls /dev/input -al`; in this list you should see `js0`. If you do not, ensure the controller is not flashing light blue.

## Receiving PlayStation Controller Events in Python

### Installing pyPS4Controller

Before running any Python, we need to install `pyPS4Controller`. To do this, execute `pip install pyPS4Controller`.

In an interactive Python session, you should be able to execute `from pyPS4Controller.controller import Controller` with no error.

### Getting Events

Here is a sample modified from the [pyPS4Controller docs](https://github.com/ArturSpirin/pyPS4Controller):

```python
from pyPS4Controller.controller import Controller

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
       print("x button pressed!")

    def on_x_release(self):
       print("x button released!")

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=60)
```

Creating a new Python file, adding the above and executing it, should print out "x button pressed!" when you press x and "x button released!" when you release x.

Use Ctrl+C to stop the script.

### Detecting More Events

Look at [https://github.com/ArturSpirin/pyPS4Controller](https://github.com/ArturSpirin/pyPS4Controller) for more usage and events you can detect. Look at the [`Action` class here](https://github.com/ArturSpirin/pyPS4Controller/blob/724c87d5d2449b192e8ee697da5b5c61d11613e4/pyPS4Controller/controller.py#L6) for how to use each function (as some provide values - like triggers and joysticks).

[From this class](https://github.com/ArturSpirin/pyPS4Controller/blob/724c87d5d2449b192e8ee697da5b5c61d11613e4/pyPS4Controller/controller.py#L6), we can see `MyController` can be expanded to handle more events:

```python
class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

     def on_x_press(self):
        print("on_x_press")

    def on_x_release(self):
        print("on_x_release")

    def on_triangle_press(self):
        print("on_triangle_press")

    def on_triangle_release(self):
        print("on_triangle_release")

    def on_circle_press(self):
        print("on_circle_press")

    # ...
```

## Disconnecting the Controller

1. Execute `bluetoothctl` in a terminal
2. Execute `disconnect [MAC_ADDRESS]`
3. Execute `exit`

Disconnecting the controller will also turn it off.

## Connecting Controller Again Later

If your Raspberry Pi was the last thing your controller connected to, holding the PlayStation button until it starts flashing light blue will allow it to automatically connect back to the Raspberry Pi. This is because the Raspberry Pi has trusted the controller and the controller automatically connects to the last thing it connected to.

If your Raspberry Pi was not the last thing the controller connected to, you will only need to use `connect MAC_ADDRESS` (within `bluetoothctl`).

## Further pyPS4Controller Usage

### All Events Available

These are all the events you can handle with functions:

```python
class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        print("on_x_press")

    def on_x_release(self):
        print("on_x_release")

    def on_triangle_press(self):
        print("on_triangle_press")

    def on_triangle_release(self):
        print("on_triangle_release")

    def on_circle_press(self):
        print("on_circle_press")

    def on_circle_release(self):
        print("on_circle_release")

    def on_square_press(self):
        print("on_square_press")

    def on_square_release(self):
        print("on_square_release")

    def on_L1_press(self):
        print("on_L1_press")

    def on_L1_release(self):
        print("on_L1_release")

    def on_L2_press(self, value):
        print("on_L2_press: {}".format(value))

    def on_L2_release(self):
        print("on_L2_release")

    def on_R1_press(self):
        print("on_R1_press")

    def on_R1_release(self):
        print("on_R1_release")

    def on_R2_press(self, value):
        print("on_R2_press: {}".format(value))

    def on_R2_release(self):
        print("on_R2_release")

    def on_up_arrow_press(self):
        print("on_up_arrow_press")

    def on_up_down_arrow_release(self):
        print("on_up_down_arrow_release")

    def on_down_arrow_press(self):
        print("on_down_arrow_press")

    def on_left_arrow_press(self):
        print("on_left_arrow_press")

    def on_left_right_arrow_release(self):
        print("on_left_right_arrow_release")

    def on_right_arrow_press(self):
        print("on_right_arrow_press")

    def on_L3_up(self, value):
        print("on_L3_up: {}".format(value))

    def on_L3_down(self, value):
        print("on_L3_down: {}".format(value))

    def on_L3_left(self, value):
        print("on_L3_left: {}".format(value))

    def on_L3_right(self, value):
        print("on_L3_right: {}".format(value))

    def on_L3_y_at_rest(self):
        print("on_L3_y_at_rest")

    def on_L3_x_at_rest(self):
        print("on_L3_x_at_rest")

    def on_L3_press(self):
        print("on_L3_press")

    def on_L3_release(self):
        print("on_L3_release")

    def on_R3_up(self, value):
        print("on_R3_up: {}".format(value))

    def on_R3_down(self, value):
        print("on_R3_down: {}".format(value))

    def on_R3_left(self, value):
        print("on_R3_left: {}".format(value))

    def on_R3_right(self, value):
        print("on_R3_right: {}".format(value))

    def on_R3_y_at_rest(self):
        print("on_R3_y_at_rest")

    def on_R3_x_at_rest(self):
        print("on_R3_x_at_rest")

    def on_R3_press(self):
        print("on_R3_press")

    def on_R3_release(self):
        print("on_R3_release")

    def on_options_press(self):
        print("on_options_press")

    def on_options_release(self):
        print("on_options_release")

    def on_share_press(self):
        print("on_share_press")

    def on_share_release(self):
        print("on_share_release")

    def on_playstation_button_press(self):
        print("on_playstation_button_press")

    def on_playstation_button_release(self):
        print("on_playstation_button_release")
```

> This is slightly modified from [controller.py in pyPS4Controller](https://github.com/ArturSpirin/pyPS4Controller/blob/724c87d5d2449b192e8ee697da5b5c61d11613e4/pyPS4Controller/controller.py)

### Stop Printing For Events I Don't Want

You may have noticed that even though you didn't add a `print` to an event, it still prints out. This is because the library does this by default. To stop this, you can create a class that overrides all of these calls with nothing. Then inherit this class that does nothing and set your events on that.

Here is what I use:

```python
from pyPS4Controller.controller import Controller


class SilencedPyPS4Controller(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        pass

    def on_x_release(self):
        pass

    def on_triangle_press(self):
        pass

    def on_triangle_release(self):
        pass

    def on_circle_press(self):
        pass

    def on_circle_release(self):
        pass

    def on_square_press(self):
        pass

    def on_square_release(self):
        pass

    def on_L1_press(self):
        pass

    def on_L1_release(self):
        pass

    def on_L2_press(self, value):
        pass

    def on_L2_release(self):
        pass

    def on_R1_press(self):
        pass

    def on_R1_release(self):
        pass

    def on_R2_press(self, value):
        pass

    def on_R2_release(self):
        pass

    def on_up_arrow_press(self):
        pass

    def on_up_down_arrow_release(self):
        pass

    def on_down_arrow_press(self):
        pass

    def on_left_arrow_press(self):
        pass

    def on_left_right_arrow_release(self):
        pass

    def on_right_arrow_press(self):
        pass

    def on_L3_up(self, value):
        pass

    def on_L3_down(self, value):
        pass

    def on_L3_left(self, value):
        pass

    def on_L3_right(self, value):
        pass

    def on_L3_y_at_rest(self):
        pass

    def on_L3_x_at_rest(self):
        pass

    def on_L3_press(self):
        pass

    def on_L3_release(self):
        pass

    def on_R3_up(self, value):
        pass

    def on_R3_down(self, value):
        pass

    def on_R3_left(self, value):
        pass

    def on_R3_right(self, value):
        pass

    def on_R3_y_at_rest(self):
        pass

    def on_R3_x_at_rest(self):
        pass

    def on_R3_press(self):
        pass

    def on_R3_release(self):
        pass

    def on_options_press(self):
        pass

    def on_options_release(self):
        pass

    def on_share_press(self):
        pass

    def on_share_release(self):
        pass

    def on_playstation_button_press(self):
        pass

    def on_playstation_button_release(self):
        pass


class MyController(SilencedPyPS4Controller):
    def __init__(self, **kwargs):
        SilencedPyPS4Controller.__init__(self, **kwargs)

    def on_R1_press(self):
       print("R1 was pressed")

    def on_L1_press(self):
       print("L1 was pressed")

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=60)
```

Now when I run this, it will only `print` when I press R1 or L1 - doing any other action on the controller will not `print` now.

## Credits

- [Feature image by Claudio Schwarz](https://unsplash.com/photos/black-sony-ps-4-game-controller-8qkQUtBQiTg)