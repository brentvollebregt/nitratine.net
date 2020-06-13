---
templateKey: blog-post
title: "Issues When Using auto-py-to-exe"
date: 2018-11-17T12:00:00.000Z
category: General
tags: [python, pyinstaller]
image: feature.png
description: "After helping many of people fix issues with auto-py-to-exe and PyInstaller, this post contains what I think you should understand and ways to fix issues you are having with auto-py-to-exe."
disableToc: false
hidden: false
---

## Introduction
A while ago I wrote an article on common issues when using [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe). In this post, I aim to replace that post and explain more in greater depth.

Please do not feel offended if I have referred you to this page, it's just the case that many other people have asked the same question you are asking and you haven't been able to find the answers I or others have provided.

### A Small Disclaimer
I cannot guarantee this post or any advice I give will fix all your issues with auto-py-to-exe and [PyInstaller](http://www.pyinstaller.org/). This tool allows you to select options and give data to be fed into PyInstaller, that means that a lot of the errors that occur will be raised by PyInstaller, meaning I can't go and change how it works. Typically though, errors brought up in PyInstaller are due to incorrect configuration, thus this post aims to help you fix anything set up incorrectly.

If you have an issue that isn't mentioned in this post, chuck it in the comments below and I will look into adding it if we can find a solution.

## What is auto-py-to-exe?
auto-py-to-exe is a project I made in my free time to make packaging Python scripts to an executable/bundle easier. The interface uses Chromes app mode and a small Python server in the backend.

When the user presses "Convert .py to .exe", all the data in the interface is sent to PyInstaller and then the output from PyInstaller is sent back to the interface. auto-py-to-exe then cleans things up in the background when done (files/folders generated by PyInstaller) and allows you to find your project in the output folder in your current working directory.

## Installation
To install auto-py-to-exe, make sure you have Python 2.7 or above installed. Ideally, you will also want Chrome installed but this is not a must; it will open in your default browser and the only thing different will be the interface size. Execute the following in the command prompt / terminal to install auto-py-to-exe:

```console
python -m pip install auto-py-to-exe
```

Wait for this to finish and make sure that the last line contains "Successfully installed auto-py-to-exe" dash some version. You might get a message about your version of pip but you can ignore it. Now to run the project, execute the following in the terminal:

```console
auto-py-to-exe
```

This will open auto-py-to-exe and the output will be saved in output/ in where your current working directory is.

### Possible Gevent Issue
There could be a situation when installing auto-py-to-exe that you are told you require Microsoft Visual C++ Build Tools. This occurs because the file that was downloaded from [PyPI](https://pypi.org/) to be installed needs to be built and these tools will build it.

Generally, the way to fix this would be to install the tools and run it again, but instead, you can get a pre-built version. To do this, go to gevents PyPI page and click "Download files" on the right to bring you to [the files that are on PyPI for this project](https://pypi.org/project/gevent/#files). You will want to find the file that matches your setup and is a .whl file, for example, I am using Python 3.7 on Windows so I would look for cp37 in the "Python version" column, Wheel in the "File type" column and then in the files that match these two criteria, match my OS - Windows. This means the file I will want is gevent-1.3.7-cp37-cp37m-win_amd64.whl (currently gevent is at 1.3.7).

## The Layout of the Interface and What Things Do

<img src="https://nitratine.net/posts/auto-py-to-exe/empty-interface.png" alt="auto-py-to-exe empty interface" style="max-height: 400px;" />

At the top of the interface, you are asked for the script location. This is the script you call to run your project, so if your project is one script, put that here, if your project is more than one script, put the script that starts it here. The inputs outline will become blue if the file exists, otherwise it will be red.

Next, you need to choose between one-file and one-directory. These are relatively similar but when using one-file with extra files like images or data files you need to modify your script to account for path changes. The difference between these methods and people ignoring the extra step required generally result in the bulk of complaints I get.

Under that is a selection of whether you want a console window to appear or not. Simply if you are developing a GUI application or something that doesn't need the console to appear, use "Window Based". If you do want the console to appear, keep "Console Based Selected" but keep in mind that the script needs to block somewhere otherwise execution will end and the terminal will disappear immediately; a workaround for this is to put `input()` at the end of the script to hold execution until input is provided.

After this, you can select an icon for your executable. Make sure that the files are .ico and don't just rename a file to be a .ico, that is not how file types work.

Next, there is a section to add files to your executable that are not Python files. Since PyInstaller doesn't find extra files like images you need to add them manually. When adding an entry, the file path/folder path needs to the in the box on the left and the destination on the right; the destination is the folder in the executable. 

- If you put a folder on the left, all files will be placed in the folder (and sub-directories keeping structure) specified on the right. 
- If you put a file on the left, this file will be put in the folder specified with the filename the same as the original.

If you're using one-file mode, you'll be provided a [link to stackoverflow](https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741) which tells you how to implement a small wrapper to find the files you added. I explain why you have to do this [towards the bottom of this post](#additional-information-and-explanations) including an example; **if you do not follow this step errors will occur**.

Under this is the advanced tab which holds all PyInstallers extra flags as well as where to save the project and setting the maximum recursion depth. Here are a few flags/options that can help with things:

- **--name**: The name of the output folder/executable
- **--hidden-import**: If the executable says a module is missing, make sure you have it installed and add it here; you can separate multiple modules by a comma.
- **--debug**: Set this to `all` to help make debugging a lot easier

The last tab is for auto-py-to-exe specific settings:

- **Output Directory**: The directory that the output of the application is put into.
- **Increase Recursion Limit**: If a RecursionError occurs, make sure this is enabled to set the depth to 5000.
- **Manual Argument Input**: A simple input to manually add to the current command.

The "Current Command" section tells you what would be called if you wanted to execute this in a terminal and the convert button is under this. After the conversion, you can clear the output or open the output folder where the executable/package was saved.

## General Steps
The process of packaging a Python project to an executable is simple in most cases.

1. Start auto-py-to-exe by executing `auto-py-to-exe` in the terminal
2. Search for your script
3. Decide on whether you want the output to be a single executable or a directory (a directory has many benefits discussed later)
4. Decide if you want a console window or not
5. Add an icon if you desire
6. Add any extra files your project requires that aren't Python files (e.g. images, csv, databases, ...)
7. Click the big blue button at the bottom to package the project
8. Open the location of the executable/package and run it

If you have any issues with running your script, it may be due to incorrect configuration. This means you will now have to go through a debugging process to find what is occurring.

## Debugging
To debug, make sure you have set up the fields in auto-py-to-exe like you had previously - all your extra files and other settings. Now go to the "Advanced" section and under the title "How to generate" put `all` in the box beside --debug. This will print out messages to the console to help you debug.

When debugging, make sure you select the "Console Based" button and using "One Directory" will help remove basic problems; you can switch back to "One File" when there are no more bugs and then fix the ones associated with "One File" mode. When all bugs are removed, you can go back to "Window Based" if you wish.

Re-package your project and open up the command prompt / terminal and [cd](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands) to the directory where the executable / package was output to. If you are using one-directory cd into that directory. Now execute `./my_project.exe` *(substitute the names)*. This will run the executable file and any errors you were missing before will be output to the console and preserved.

Look at what these errors are saying and fix them. Now repackage like you just did and keep fixing bugs and repackaging until there are no more left and your project is working properly. After this, you can then move to one-file if you were using one-directory and want one-file, and repeat the process by still staring it with cmd and debugging on.

When everything is done and there are no more bugs in the modes you want, you can enable "Window Based" if you want and remove `all` from --debug.

> Not every project can be converted to one-file. This is due to files being used by the application being lost every time the application starts/stops. To understand this more go down to ["Demonstration of Files References After Packaging"](#demonstration-of-files-references-after-packaging).

### How to Fix Specific Issues
These are some of the issues I have come across or others have asked me about and ways to fix them.

#### Fatal Error: failed to execute <script.py>
This means something has gone wrong as it's giving you a visual warning about it; this is not an error, it's a warning; the real error has been printed to stdout/stderr. If you open the executable using the terminal or something else that will preserve the console output, you will most likely see a Python error telling you what went wrong. Fixing this and repackaging is the solution to this issue.

#### PermissionError: [Errno 13] Permission denied: ...
This occurs because you are trying to modify files in a directory you do not have access to. A way to fix this is to run the script with admin privileges by opening cmd as admin and then running `auto-py-to-exe` one you have cd'ed to the directory you want the output to be in.

One reason this could occur is that you have opened cmd and am in System32. Make sure you do not accidentally modify files in this directory so make sure you are in a directory where you want to write files to when running `auto-py-to-exe`.

#### RecursionError
This error is now prevented by the application by default by setting the recursion limit to 5000. If you want to disable this, there is an option in the *Settings* tab to.

#### AttributeError: module 'enum' has no attribute 'IntFlag'
Try executing `python -m pip uninstall enum34` to stop enum conflicts. This is also a fix for the similar issue "Fatal Python error: Py_Initialize: unable to load the file system codec".

#### ModuleNotFoundError: No module named x / ImportError: No module named x
This means a particular module ('x' in this case) was not added to the package. I have seen this occur with packages in the pandas library and win32api; as long as you can identify the package (e.g. 'x'), then it is very easy to fix.

To fix this in the UI, open the advanced tab and find the `--hidden-import` input. Simply paste the module name into this input and then repackage. If the original error is still appearing, you have done this incorrectly.

For example, if you are missing `pandas._libs.tslib`, add 'pandas._libs.tslib' into the input by --hidden-import. Additionally, you can add more than one module, for example, `pandas._libs.tslib, win32api`. *(See the question mark by the input for more information)*.

#### ERR_CONNECTION_REFUSED
You need to be connected to the internet. This error appears when you cannot reach the servers.

#### Command "python setup.py egg_info" failed with error code 1
Update setuptools using `pip install --upgrade setuptools`.

#### FileNotFoundError
Make sure the file you are referencing actually exists, this error says that the file you are referencing doesn't exist. If you are using one-file mode, make sure you have followed the necessary steps.

#### struct.error: unpack requires a buffer of 16 bytes
This typically occurs when you have supplied `--icon` / `-i` with a file that is not a `.ico` file. Please note that simply changing the extension of a file to .ico does not make it a .ico file; you will need to use a converter of some sort to convert your file (e.g. png, jpg) into a .ico.

## General Questions Constantly Asked

### How do I Convert All My Python Files?
Add the entry point in the script location. PyInstaller searches for imports to get the rest of the Python files required to run, so as long as you use the `import` keyword, your files will be added.

### The Terminal Just Opens and Closes But There Are No Errors
If you double click to run your Python script, what happens? Does it open and close also? That means this tool has done its job correctly and the script is finishing just like it should.

You most likely think the output should stay visible because you are always using IDLE or an IDE and that's what those tools do. Add a statement like `input()` at the end of your script to block execution and wait for you to press enter before closing. 

Alternatively, there may be an error occurring which means you need to follow the debugging steps above.

### 'python'/'pip'/'auto-py-to-exe' is not recognised as an internal or external command, operable program or batch file.
This occurs because the path that these executables are located in is not on your path; thus cmd doesn't know where to look for them. You need to add these paths to the PATH environment variable so cmd knows where to look for the executable you are trying to execute.

I created a script that can help set up these paths automatically, which can be found in my "[Fix: 'python' is not recognized as an internal or external command](/blog/post/fix-python-is-not-recognized-as-an-internal-or-external-command/)" post. 

If you want a more manual approach to understand what is occurring, watch my [video on how to setup Pythons PIP](https://youtu.be/cm6WDGAzDPM). This will show you how to add the `\Scripts` folder, but I also recommend you add the root Python directory (same path without '\Scripts') so the `python` command will work. The paths you will need to add can be found using the commands below:

```python
import os, sys

# If 'python' is not recognised
print (os.path.dirname(sys.executable))

# If 'pip'/'auto-py-to-exe'/... is not recognised
print (os.path.dirname(sys.executable) + "\\Scripts")
```

> If you are using something older than Windows 10, setting the PATH environment variable will be a bit different than what is demonstrated in the video. If it is just one line, add a `;` to the end and then paste the path after the `;`.

### The exe Doesn't Work on Another Computer
This may be an architecture issue. PyInstaller will build an executable using the architecture of the machine it was built with. This means if you are using a 32bit machine, it will create a 64bit executable. As with any other programs, you cannot run 64bit on 32bit but you can run 32bit on 64bit. Thus I recommend using 32bit python or compiling on a 32bit machine so it will work on both architectures.

### What is the \_\_pycache\_\_ folder?
This is [Python bytecode generated by Python](https://stackoverflow.com/questions/16869024/what-is-pycache). You can delete this if you wish.

### My Antivirus Detected the exe as a Virus
This is your anti-virus vendors fault. Check out [this](https://github.com/pyinstaller/pyinstaller/issues/2501#issuecomment-286230354). There is nothing I or PyInstaller can do to stop this.

### Lots of Warnings Appear in the Output
These warnings can be ignored in most cases. I have not currently found a situation where these are an issue, after all, they are only warnings. These warnings typically match the format `WARNING: lib not found: api-ms-win-crt-<specific dll> dependency of <file>`.

A YouTube user comment on the video related to this project that if you add `C:\Windows\System32\downlevel` to your PATH variable, these DLLS that were previously not being found can now be found. This is because the files missing are commonly found in this folder. Adding this folder to your path to now successfully locate these files can also speed up packaging times.

### "VCRUNTIME140.dll" is either not designed to run on Windows or it contains an error
Try selecting the `--noupx` button in the advanced tab.

## Additional Information and Explanations
Some things that are clear to people that use Python a lot are not always clear to new people. Here are some discussions about why and how things occur.

### Using `concurrent.futures`
It was brought to my attention by [William Lake](https://github.com/William-Lake) in [this GitHub issue](https://github.com/brentvollebregt/auto-py-to-exe/issues/67) that when using `concurrent.futures` for any multi-threading/processing, it is recommended to add the following import:

```python
from multiprocessing import freeze_support
```

and this line to your main:

```python
freeze_support()
```

William had stated that before adding these lines, he kept getting errors regarding `concurrent.futures` even though it worked fine before packaging.
 
> [A related issue on bugs.python.org recommending the fix](https://bugs.python.org/issue21505)

### The Difference Between One Directory and One File
One directory puts all your files in one folder. You can easily add and remove files like you normally would in a folder. When your script modifies a file in its folder, the file will still be modified when you run the script again.

One file mode is a bit different, instead of putting all the files in a folder, it puts them in something like a zip file which is contained in the end executable. When you run the executable, the files contained internally are unpacked to a new temporary directory. Due to one file unpacking on startup, it is a lot slower to start.

Also due to the files being unpacked to a new temporary directory on execution, the files that you modified added that were in the same directory as the executable will not be there on the next run because they are now in a different unknown folder. This means when creating files, you will want to use an absolute path that is not where the project files are (could use something like APPDATA on Windows).

#### Demonstration of Files References After Packaging
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

### The one-file Resource Wrapper
As described in the section above, non-python files that are bundled into an executable when using one-file mode need care when being referenced due to how they are un-packaged.

In the interface, when one-file mode is selected and the additional files section is expanded, a note can be found that references a StackOverflow question regarding ["Bundling data files with PyInstaller (--onefile)"](https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile). The first answer provides a nice snippet of code:

```python
import sys, os
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
```

When referencing files using *relative references*, instead of using `open('folder/my-file.jpg')`, you will want to use `open(resource_path('folder/my-file.jpg'))`. This appends the relative path you provided to the current / extracted location to make an absolute file reference which is safe to use.