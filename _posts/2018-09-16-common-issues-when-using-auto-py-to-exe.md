---
layout: post
title: "Common Issues When Using auto-py-to-exe"
date: 2018-09-16
categories: General
tags: Python pyinstaller
description: "In this post I will go over how to install auto-py-to-exe, talk about how it works and demonstrate how to use it. I will also cover commonly asked questions and issues that people run into and how to fix them."
---

* content
{:toc}

In this post I will go over how to install auto-py-to-exe, talk about how it works and demonstrate how to use it. I will also cover commonly asked questions and issues that people run into and how to fix them. The point of this post is to help people understand why they are having their issues.

<!-- more -->

## Installation
First make sure you have Python 2.7 or above. Currently auto-py-to-exe supports up to and including Python 3.7.
You can check if any others versions of Python are supported by going to the [projects GitHub page](https://github.com/brentvollebregt/auto-py-to-exe).

Open cmd and execute `python -m pip install auto-py-to-exe`. Wait for this to finish and make sure that the last line contains "Successfully installed auto-py-to-exe" dash some version. You might get a message about your version of pip but you can ignore it. If you got an error saying python isn't recognised as a command then make sure the directory that python.exe is located in is in your PATH variable; you can look at some solutions [here](https://stackoverflow.com/questions/17953124/python-is-not-recognized-as-an-internal-or-external-command) if you are unsure how to do that.

Ideally you will also want chrome installed but this is not a mus; it will open in your default browser and the only thing different will be the interface size if you don't have chrome.

To make sure you have installed auto-py-to-exe correctly, go back into cmd and execute `auto-py-to-exe`; this should open the interface.

## What Does PyInstaller Do?
auto-py-to-exe uses PyInstaller to package the Python interpreter, required files, your Python files and any other files you supply it into a package which can be run by running the executable produced. This means it will look at the script you provide as the starting point and then look at the imports recursively finding what Python modules it needs to include. So if you have created your own Python scripts and imported them, they will be packaged like any other Python module.

PyInstaller does not find other files like images and data files due to the possible dynamic nature of the files. To add files like images or data files, they need to be added in the interface as I will show soon.

### The Difference Between One Directory and One File
One directory puts all your files in one folder. You can easily add and remove files like you normally would in a folder. When your script modifies a file in it's folder, the file will stay changed when you run the script again.

One file mode is a bit different, instead of putting all the files in a folder, it puts them in something like a zip file which is contained in the end executable. When you run the executable, the files contained internally are unpacked to a new temporary directory. Due to one file unpacking on startup, it is a lot slower to start.

Also due to the files being unpacked to a new temporary directory on execution, your modified/added files will not be there on the next run because they are now in a different unknown folder. This means when creating files, you will want to use an absolute path that is not where the project files are (could use something like APPDATA on Windows).

When packaging a script for the first time, I recommend to use one directory and make sure there are no errors. After that you can then package it to one file and solve any issues, using this method. Remember you don't have to make a package one file, a lot of the time it is better to leave as one directory.

> Do remember that when using relative directories for file names, these are **relative to the current working directory**, not the location of the programs files. This is exactly the same as when you use a Python script normally. So depending on where you run the executable from, relative files my end up in different places.

#### Demonstration of Files Being Extracted
I made a small Python file that finds where it is located and then tries to print the contents of a file if it exists otherwise will create a new one.

```python
import sys, os
if getattr(sys, 'frozen', False): # we are running in a bundle
    bundle_dir = sys._MEIPASS # This is where the files are unpacked to
else: # normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

print ('Location : ' + bundle_dir) # Where the base file exists

file = bundle_dir + '\\test.txt'
print ('File is at: ' + os.path.abspath(file)) # Absolute path of target file
if os.path.isfile(file):
    with open(file, "r") as f:
        print ('Contents:\n' + f.read()) # Print contents of file if it exists
else:
    print ('Created a new file') # Create a file if it doesn't exist

with open(file, "a") as f:
    f.write('New Line\n') # Add a new line to see if is there next time

input() # Block to keep terminal alive
```

##### Running this un-packaged (.py)
The first time it will create a file beside the script. Every time it is run, the new line will be added and this will be shown in the output. This means When you modify a file, it will stay modified.

##### Running this when packaged using one directory
The first time it will create a file in the directory (which will be beside the .exe). Every time it is run, the new line will be added and this will be shown in the output. This means When you modify a file, it will stay modified.

##### Running this when packaged using one file
Every time this is run, it will create a new file in the temporary directory. This occurs because the .exe unpacks to a new directory every time it is run, so instead of finding old files (which can disappear any time because they are in the temp folder) you may as well use an absolute reference to somewhere else.

### Console vs. Window Based
The second set of buttons in the GUI is to choose whether your script should show a console. If you don't need to show a console then you can select the window based button.

If you are debugging at all, you will need to keep the console based button selected to output is directed to the console instead of pop-up windows for each line.

## Basic Usage
So finally, now that all of that is out of the way, you can package something.

First open the GUI using the command `auto-py-to-exe` and search for your file. The input box outline will become blue when the file exists. Next select one directory or one file and if you want a console window.

You can then add an icon if you want by expanding the icon section (click on the chevron) and search for a .ico file. Make sure you not don't just rename an image file to .ico, extensions basically mean nothing so doing this will do nothing except cause errors. Convert png/jpeg/bmp to ico properly using online tools. (I see way too many people think this is ok).

If your script uses any external files like images or data files that are not Python files (.py, .pyw....), you must add them in the "Additional Files" section; if you do not do this, PyInstaller will not package those files. You can choose to add multiple files, a single folder or manually add them. The input box to the left is where the files are coming from and the input box to the right of it is the destination. Keep the destination paths relative to the root of the script, so that means if you want an image right beside the executable, use '.' and if you want a file in images/ then put 'images/' into the input box.

> If you use a file in the "Additional Files" section, this references all the images in the folder. This means every individual file will be moved to the destination individually. To keep the files in a folder still, use the folder name as the destination (don't forget /).

## Debugging
As with any sort of development, bugs will occur and debugging will need to take place. To enable debugging, go into the "Advanced" section and under the title "How to generate" put 'all' in the box beside --debug. This will print out messages to the console to help you debug.

When debugging, make sure you selected the "Console Based" button and using "One Directory" will help remove basic problems; you can switch back to "One File" when there are no more bugs and then fix the ones associated with "One File".

After re-packaging your project, open up cmd, use the cd command to change directories to where the exe is located and then execute `./my_project.exe` (substitute the names). This will run the executable file and any errors you were missing before will be output to the console.

Fix the errors that appeared and then re-package. Keep executing with debugging mode and fixing errors until there are no more errors.

## General Questions
Here is a list of general questions I get asked a lot and the answers to them

### How Can I Make Two Executables Use the Same File?
You will need to construct a path before packaging them that both scripts agree on. Now both scripts can write/modify files in that path and the other executable will know where to find them.

### The Console Just Appears And Disappears
People that use IDLE all the time don't always understand that these scripts don't wait for the user; once they are finished, they finish. What's occurring is either your script is causing an error (which you would have found out with --debug so this question isn't for you) or it has just finished. One way to check if the latter is occurring is to put `input()` at the end of your script. Now when it finishes, it will wait for you to press enter because input() is a blocking statement (.run() methods for servers are generally blocking so that is why they don't end).

### Permissions Denied?
You are most likely running in a directory where you haven't given the script enough privileges to modify files. Run auto-py-to-exe using a cmd with admin privileges so it can modify these files.

### My Package isn't working on a particular computer?
This could be due to the operating system or the architecture (what bit). Make sure you are using the same operating system you packaged your script with. If it is the same operating system, then it may be an issue with the architecture you are using.

Pyinstaller will create an executable with the architecture of the machine it was built with. If you use a 64bit machine to compile the .py, it will create a 64bit executable. As with any other programs, you cannot run 64bit on 32bit but you can run 32bit on 64bit. Thus I recommend using 32bit python or compiling on a 32bit machine so it will work on both architectures﻿ (or package twice for each architecture).

### ModuleNotFoundError
I have been asked about many issues regarding `"ModuleNotFoundError: No module named 'pandas._libs.tslib'"`; this is because PyInstaller hasn't seen that this pandas._libs.tslib is required.

To fix this, add "--hidden-import=pandas._libs.tslibs" as an extra flag at the bottom of the advanced tab﻿. This will tell PyInstaller to include it when packaging.
