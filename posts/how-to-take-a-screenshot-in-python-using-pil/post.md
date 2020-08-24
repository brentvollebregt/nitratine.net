title: "How To Take A Screenshot In Python Using PIL"
date: 2020-08-24
category: Tutorials
tags: [python, pil]
feature: screenshot-main-monitor.png
description: "In this tutorial, I will demonstrate how to take a screenshot using PIL in Python. Window, macOS and Linux are all supported."

[TOC]

## What Is PIL?

PIL (Python Imaging Library) is a Python library that adds support for opening, manipulating, and saving many different image file formats. It has a very friendly API with lots of help online including [good documentation](https://pillow.readthedocs.io/en/stable/index.html). 

PIL supports Windows macOS and Linux and supports many versions of Python; see the installation notes to identify which version of PIL you will need for the version of Python you are using. At the time of wiring this, PIL 7 has been released and supports Python 3.8 - 3.5.

## Installing PIL
To install PIL, execute the following in a terminal:

```terminal
python -m pip install pip
```

> To install an older version of PIL, execute `python -m pip install pip=<version>` eg. `python -m pip install pip=7.2.0`. You can find older versions released in the [release notes](https://pillow.readthedocs.io/en/stable/releasenotes/index.html).

To validate it was installed correctly, go to IDLE or a python shell and execute:

```python
import PIL
```

If no import error is raised, it was installed successfully.

### I Can't Import PIL
Make sure you have executed the install command above; if you're not sure you have executed it already, it is safe to execute it a second time.

If there were no errors when installing it and it says PIL is installed successfully, make sure you're 100% sure that you installed PIL in the same distribution of Python that you're trying to import it in. Go to my tutorial on [How to Manage Multiple Python Distributions](https://nitratine.net/blog/post/how-to-manage-multiple-python-distributions/) if you're having some issues or are unsure about this.

## Taking A Screenshot
To take a screenshot, we first need to import the [`ImageGrab`](https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html) module from PIL.

After we have the `ImageGrab` module, we can call `.grab()` to take a screenshot

```python
from PIL import ImageGrab

screenshot = ImageGrab.grab()
```

> On Linux, you must be using PIL 7.1.0 or higher for this to work; [see release notes](https://pillow.readthedocs.io/en/stable/releasenotes/7.1.0.html#x11-imagegrab-grab).

### Viewing The Screenshot
To view the screenshot, we can call `.show()` on the returned [Image object](https://pillow.readthedocs.io/en/stable/reference/Image.html). For example, using the code from above:

```python
from PIL import ImageGrab

screenshot = ImageGrab.grab()
screenshot.show()
```

Executing this will open the screenshot in your default image viewer. If you have more than one display, you will notice that this screenshot is only of the first display; I will expand on this further [below](#taking-a-screenshot-of-a-different-display).

Here is an example of a screenshot I took:

![Screenshot Main Monitor](/posts/how-to-take-a-screenshot-in-python-using-pil/screenshot-main-monitor.png)

### Saving The Screenshot
Saving images in PIL is very easy, calling `.save()` on the returned Image object will allow us to save the image into a file. 

```python
from PIL import ImageGrab

filepath = 'my_image.png'

screenshot = ImageGrab.grab()
screenshot.save(filepath, 'PNG')  # Equivalent to `screenshot.save(filepath, format='PNG')`
```

Now if you go and open the file `filepath` ("my_image.png" in the current working directory for this example), you will see the screenshot has been saved.

> If you provide a file path with an extension of a supported image format, you can omit the format.

#### Saving To A File Object
If you have a file already open in write mode or want to save the image to a file object, you can pass that instead of the filename. For example:

```python
from PIL import ImageGrab

file = open('my_file.png', 'w')

screenshot = ImageGrab.grab()
screenshot.save(file, 'PNG')  # Save the image to the file object as a PNG

file.close()  # Make sure to close the file when you're done
```

or

```python
from io import BytesIO
from PIL import ImageGrab

bytes_io = BytesIO()

screenshot = ImageGrab.grab()
screenshot.save(bytes_io, 'PNG')  # Save the image to bytes_io as a PNG

# Do what you want with the bytes_io object
```

## Taking A Screenshot Of A Different Display
Back when we took a screenshot using `ImageGrab.grab()`, it only captured the main display. To take a screenshot of all displays, we can pass `all_screens=True`:

```python
from PIL import ImageGrab

screenshot = ImageGrab.grab(all_screens=True)
```

> Please note that `all_screens` is currently only supported in Windows

Now when you call `screenshot.show()`, you will see that multiple monitors are now displayed. Here is an example of my monitors:

![Screenshot All Monitors](/posts/how-to-take-a-screenshot-in-python-using-pil/screenshot-all-monitors.png)

Now that you have this larger image, you can crop it using other methods in PIL: [How to crop an image using PIL](https://stackoverflow.com/a/58350508).
