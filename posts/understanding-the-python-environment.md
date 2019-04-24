title: "Understanding The Python Environment"
date: 2019-04-15
category: General
tags: [python]
feature: feature.png
description: "For people new to Python, locating Python files for development can be confusing; these can be python.exe, the scripts folder and even the location of where modules are installed to. In this post I'll discuss where to look for particular files and how to debug some common issues relating these confusions."
hidden: true

[TOC]

## Locating Your Instillation
When first installing Python, depending on what you select in the installation, there are a couple of places Python could be installed (you could also select your own directory). Luckily this can be easily found by executing the following in Python:

```python
import sys
print(sys.executable)
```

This will print the location of python.exe which is the executable that 

Common places:
 - C:\PythonXY
 - %AppData%\Roaming\Python\PythonXY
 
## Root Directory
- Contents

### python.exe vs pythonw.exe
- windowed vs not windowed
- Calling the different types -> .py vs .pyw

## DLLs/
- Folder contains dlls. .pyd are 
    - Python dll files; "If you have a DLL named foo.pyd, then it must have a function initfoo()." 
    - https://docs.python.org/2/faq/windows.html#is-a-pyd-file-the-same-as-a-dll

## include/
- Header files (.h) for Python/C API.

## Lib/
- Standard library
- Also contains site-packages
    - Where all modules are installed to

## libs/
- Native code libraries compared to Lib/
- .lib files

## Scripts/
- Executables related to Python that allow you to do tasks usually provided by downloaded modules
- Add this to the path if it is not on there

## tcl/
- tkinter

## Tools/
- Python tools supplied in the distribution
- Examples:
    - scripts/diff.py
    - scripts/md5sum.py

## TODO
- 'python' is not recognized as an internal or external command
- Where modules are located
- The scripts folder and adding it to PATH
- python.exe vs pythonw.exe