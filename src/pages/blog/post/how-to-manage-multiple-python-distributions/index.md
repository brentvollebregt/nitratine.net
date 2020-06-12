---
templateKey: blog-post
title: "How to Manage Multiple Python Distributions"
date: 2020-05-20T12:00:00.000Z
category: Tutorials
tags: [python]
image: feature.png
description: "Having multiple distributions of Python installed and not managing them correctly can lead to confusion. In this post, I discuss how to identify this potential mess and methods to fix it."
hidden: false
---

[TOC]

## The Issue / Potential Confusion
Quite often, I get comments from people telling me that a module doesn't work, that they have installed the library/module:

```bash
pip install xyz
```

And then executed `python file.py` which says something like the following:

```
Traceback (most recent call last):
  File "file.py", line 1, in <module>
    import xyz
ModuleNotFoundError: No module named 'xyz'
```

Two things could have happened here:

1. Installing the `xyz` module failed. This would have clearly been stated when executing `pip install xyz`.
2. When using `pip`, the module has been installed in one distribution of Python and then a different distribution of Python has been used to try and import the module.

Point 2 is what I will be focusing on in this post and how to fix confusion between more than one installed distribution of Python.

## Identification
Aside from the situation outlined above, there are better methods of proving that this is the case. The best method in my opinion, would be to identify where the `pip` and `python` executables are and check if they are in the same Python distribution. To do this, you can use the `where` command in Windows.

For example, to identify what executable is executed when I execute `python`, I would execute:

```bash
where python
```

This will print one or more paths. When I execute it for example, the following is printed:

```text
C:\Python37\python.exe
```

> Most people will find that they have only one path in this returned list. If you have more than one printed, use the top one; I discuss why more than one path may be returned later.

To find the location of pip, I would then execute:

```bash
where pip
``` 

Which would then output one or more paths. In my case, it has output:

```text
C:\Python37\Scripts\pip.exe
```

### Checking That These Executables are From the Same Distributions
Using the paths returned from these two `where` calls, you can then see if they both belong to the same distribution or not.

Typically a Python distribution has a root folder which contains python.exe and a Script folder which contains pip.exe. Using my example, you can see that my paths follow the pattern as the Python root is "C:\Python37\".

In the case you have paths that do not have a common root folder like:


```text
> where python
C:\path\to\distribution1\python.exe

> where pip
C:\a\different\path\to\distribution2\Scripts\pip.exe
```

We can see that they do not follow the Python root folder structure I described. We can also see they do not share the same parent directory so they must be from different distributions.

## How Windows Decides Which Executable to Execute
When you execute a command in a terminal, the terminal has to figure out which executable to call. As shown above, we can use the `where` command to identify which executable is found and executed.

`where` prints the paths of executables that the terminal has identified with the name you provided; the top file path is always the one that is executed.

The terminal has found these by searching the PATH environment variable. The PATH environment variable is a string that contains directories to look at when searching for executables that can be executed. This means you can make an executable/.exe available to use in cmd by adding the folder that it's located in to the PATH environment variable.

To look at your PATH environment variable, execute:

```bash
echo %PATH%
```

> To modify your PATH environment variable, look at my tutorial on [How To Setup Python's PIP](/blog/post/how-to-setup-pythons-pip/). In this post, I show you how to add a path to the PATH environment variable.

When I'm in a virtual environment and execute `where python`, I get the following output:

```text
C:\Users\Brent\GitHub\nitratine.net\venv\Scripts\python.exe
C:\Python37\python.exe
```

I now have two "python" executables I can execute, but only the top one will be used (we only need to execute one of them).

The terminal has identified these paths in this order by looking at my PATH environment variable and searching each folder listed in it for a "python" executable. Each path is searched based on its position in the PATH environment variable - paths at the start get searched first.

When not using `where`, the terminal will typically find the first executable required (first path in the list) and then stop searching as it has what it needs. This means when there are many executables with the same name in the folders to be searched, the executable found first when searching the folders in order will be executed.

## Solutions
There are a couple of common solutions that we can use to fix this mixing of distributions issue. Both these solutions use the knowledge above about how Windows finds the executables we are wanting to execute.

### Virtual Environments
This is my most recommended as you can be sure everything is where you expect it. 

Virtual environments can solve the issue we're looking at because it sets up a folder structure for its own dependencies and executables and then adds the "Scripts" path of this environment to the beginning of the PATH environment variable so that the executables within will be found instead of other executables outside the environment.

There are many tutorials on setting up virtual environments in Python and there are many different modules you can use; but here are some basics using the Python 3 built-in venv:

#### Setting Up The Virtual Environment
To set up a virtual environment, open a terminal and execute the following:

```bash
python -m venv venv_folder
``` 

This will ask Python's venv module to create a virtual environment in `venv_folder`. You can substitute `venv_folder` for a different folder name if you wish, the convention is to use a folder named `venv` but I have used `venv_folder` in this tutorial to better identify it as a folder. 

#### Activating The Virtual Environment
Before activating the virtual environment, executing `python` and `pip` will still use the globally setup distribution(s). To use the virtual environment executables, you need to activate it.

While beside the `venv_folder` folder (or whatever you named it) in cmd, execute:

```bash
venv_folder/Scripts/activate
```

> If your folder was named `venv`, call `venv/Scripts/activate` (or substitute for a different name).

Now when you execute `where python` and `where pip`, you will see that executables from this virtual environment are being used. This is because the Scripts folder in the virtual environment has been added to the start of the PATH variable; you can see this by executing `echo %PATH%` again.

#### Deactivating The Virtual Environment
To deactivate the virtual environment, go back to the same folder in cmd beside `venv_folder` and execute:

```bash
venv_folder/Scripts/deactivate
```

Executing `where python` and `where pip` again, you will see that the original setup has been restored.

Also, since these methods only modify environment variables in the session, closing the terminal session will throw away the activation. You can easily reactivate the virtual environment by following the instructions above again.
 
#### Installing Dependencies
Now that you know how to set up, activate and deactivate a virtual environment, you can use this to be sure what `python` and `pip` you are executing.

To install dependencies, use the normal `pip install xyz` and to run a Python script, use the normal `python my_file.py`.

### Setting up Your PATH Environment Variable in an Expected Way
If you don't want to deal with virtual environments, you could just set your PATH environment variable to make sure you get the correct `python` and `pip` each time.

To do this, first identify the root of the Python distribution you want to use. If you already have access to the `python` executable or IDLE you want to use, execute the following in it:

```python
import os
import sys
print (os.path.dirname(sys.executable))
print (os.path.dirname(sys.executable) + '\Scripts\\')
```

This will print out two paths; one which is the root folder for the Python distribution that is being used and the other being its Scripts folder.

Following my tutorial on [How To Setup Python's PIP](/blog/post/how-to-setup-pythons-pip/), add these two paths to the *beginning/top* of the PATH environment variable.

Now when you execute `where python` and `where pip`, `python.exe` and `pip.exe` should be found in these two folders you added first.

> When making these changes to the PATH environment variable, you can also identify folders from other Python distribution that you don't actively use and remove them from the PATH environment variable. Then to use these other distributions of Python, absolutely reference the executable in cmd, e.g. `C:/my/second/python/distribution/python.exe`.
