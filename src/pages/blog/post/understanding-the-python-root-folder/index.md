---
templateKey: blog-post
title: "Understanding The Python Root Folder"
date: 2019-06-11T12:00:00.000Z
category: General
tags: [python]
image: feature.png
description: "For people new to Python, locating Python files for development can be confusing; these can be python.exe, the scripts folder or the location of where modules are installed to. In this post, I discuss what folders host what and how to track common things down."
hidden: false
---

[TOC]

## Locating Your Installation
When first installing Python, depending on what you select in the installation, there are a couple of places Python could be installed (you could also select your own directory). Luckily this can be easily found by executing the following in Python:

```python
import sys
print(sys.executable)
```

This will print the location of python.exe which is the executable that runs Python scripts. Common places for Python to be installed on is in `C:\PythonXY` or `%AppData%\Roaming\Python\PythonXY`.

To run Python scripts, you need to pass a filename as an argument to python.exe so python.exe can run it. For example, if you wanted to execute myscript.py, you would call `python myscript.py` which calls `python.exe` (regarding it can be found on the PATH) and passes the filename "myscript.py" as an argument.

## Root Directory
Where you located python.exe is also the root of your Python installation (assuming you aren't using a virtual environment). In this folder, you will find files relating directly to Python and modules you have installed. Under the headings below, I'm going to explain what is in each of the folders in the root folder and notable subdirectories in them.

### python.exe vs pythonw.exe
Before we start looking at the folders, you should notice there is a `python.exe` and a `pythonw.exe` file. These do very similar jobs but have one primary difference, `python.exe` will open a terminal window whereas `pythonw.exe` will not.

Typically `.py` files are associated with `python.exe` and `.pyw` files are associated with `pythonw.exe`. This means if you want to see the output from your script (like `print` calls) or just want to know it's running by seeing a window open, then use `.py`, otherwise, you will want to use `.pyw` to hide the terminal window that appears.

> [Here](https://stackoverflow.com/a/30313091) is a writeup of the smaller differences between them. 

### DLLs/
The folder `DLLs/` contains DLL files relating to Python. When looking in here, you may notice that there are actually `.pyd` files in here.

`.pyd` files are actually the same as DLL files but they include a function `PyInit_MODULE()` where "MODULE" is the name of the DLL file (without the extension). You can read more about this [in the docs](https://docs.python.org/3/faq/windows.html#is-a-pyd-file-the-same-as-a-dll).

### include/
The folder `include/` contains header files for the Python/C API

### Lib/
The folder `Lib/` contains the Python standard library; that is, all the modules that come with Python like `csv`, `io`, `tkinter`, `re` and many others.

A very notable folder in this folder is `site-packages`. This is where Python modules are installed when you install them using `pip` or a `setup.py` file. Looking in this folder for a module you want to investigate can allow you to see the source.

If you import a Python module in a Python script and then print the module, the path output will typically be in this folder; for example:

```python
import flask
print(flask)
```

For me outputs `<module 'flask' from 'C:\\Python36\\lib\\site-packages\\flask\\__init__.py'>`. C:/Python36 is where Python is installed for me and you can see flask is sitting in lib/site-packages.

### libs/
The folder `libs/` contains native code libraries in comparison to `Lib/`. This means whereas most files in `Lib/` are human-readable, `libs/` typically contains compiled libraries.

> [Here](https://stackoverflow.com/a/19286879) is a bit more information on this folder.

### Scripts/
The folder `Scripts/` contains executables and other "scripts" that can be run. Typically this is where modules will put executables so they are then located in the terminal/OS calls using the [PATH variables](/blog/post/fix-python-is-not-recognized-as-an-internal-or-external-command/).

Putting executables in here allows us to easily execute a command which will be looked for in here (regarding this folder is in the PATH variable) and then executed. If you set console scripts in a `setup.py` file, the names you specify will be created as executables in here.

> [Here is an example](https://github.com/brentvollebregt/auto-py-to-exe/blob/d4130394504df7e0e4db439e6a2b0864b7b29966/setup.py#L35) of a console script that I mentioned. This allows you to call `auto-py-to-exe` on the command line to start the application.

### tcl/
The folder `tcl/` contains tkinter source files as tkinter runs on tcl. 

When packaging Python to an executable, you might find some files from here in the result folder/executable; some times it can be safe to remove these to make the package smaller in size.

### Tools/
The folder `Tools/` contains Python tools supplied in the distribution. Looking in this folder surprised me when I first saw them as they are practically examples and demos of the Python language doing something useful.

Here are some examples of these:

- `scripts/md5sum.py`: "Python utility to print MD5 checksums of argument files"
- `scripts/diff.py`: Finds the difference of two files. "Command-line interface to difflib.py providing diffs" in different formats.
- `scripts/google.py`: Open a search term in a new browser window/tab
