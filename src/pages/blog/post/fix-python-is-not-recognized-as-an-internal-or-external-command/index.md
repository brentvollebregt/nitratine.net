---
templateKey: blog-post
title: "Fix: 'python' is not recognized as an internal or external command"
date: 2019-05-15T00:00:00.000+12:00
category: Tutorials
tags: [python]
image: feature.png
description: "This is tutorial on how to fix the classic error, 'python' is not recognized as an internal or external command, operable program or batch file, when trying to call Python from a terminal"
disableToc: false
hidden: false
---

## Why You Are Getting This Error

When executing `python` or `pip` from the terminal (or whatever application you are using), if your environment isn't set up correctly, you will be given an error saying `'python' is not recognized as an internal or external command, operable program or batch file.` (or `pip` when executing `pip`).

When you execute the command `python` in the terminal, the terminal will look through all the paths on the systems PATH environment variable to look for an executable `python.exe`. Since there are no paths/folders on the PATH environment variable that contains `python.exe`, this error is shown because it does not know what executable to execute.

> Please note, these solutions will only work on Windows as it describes how to add paths to the systems PATH environment variable

## A Temporary Fix

One way to temporary fix this is to specify the full path of the executable you are trying to execute. To find the location of `python.exe`, open Python/IDLE and execute:

```python
import sys
print(sys.base_exec_prefix + '\\python.exe')
```

Copy this value that was printed and paste it in the terminal, then execute it. You will now find that this does exactly what you would expect `python` to do; that is because it's doing the same thing - executing the python executable.

> I say this is temporary because it is a lot more effort to use the full path

## A Permanent Fix

A more permanent fix would be to add the directory shown above to the systems PATH environment variable so the terminal can find it automatically; this will allow you to simply execute `python` every time.

In my post on [How To Setup Python's PIP](/blog/post/how-to-setup-pythons-pip/) I show you how to add the Script path to the PATH variable so `pip` can be found by the terminal. Replacing the path in the tutorial with the path found above will allow us to fix our `python` issue.

Instead of doing all of that manually, I wrote a script that will check if the root Python path (found above) or the Scripts path is not on the _users_ PATH variable. Using the _users_ PATH variable allows us to set everything up without requiring admin privileges. Simply executing this, reading the output and answering the one question it asks you (if action is required) will fix both paths for you.

```python
import sys
import subprocess
import os

INFO = '[INFO] '
OK = '[OK] '
ACTION = '[ACTION] '
WARN = '[WARN] '
ERROR = '[ERROR] '


def get_path():
    """ Get the users PATH environment variable """
    p = subprocess.Popen(
        ['powershell.exe', '[Environment]::GetEnvironmentVariable("PATH", "User")'],
        stdout=subprocess.PIPE,
        shell=True
    )
    out, err = p.communicate()
    return out.decode('utf-8').strip() # Get \n\r off


def folder_path_in_path_variable(target_path, path_list):
    """ Check if the target path is in a list of paths (looks for path\ also) """
    return target_path in path_list or target_path + '\\' in path_list


def add_path(_path):
    """ Add a path to the users PATH environment variable """
    # Get path value and check if it already contains the path
    current_path_value = get_path()
    if _path in current_path_value.split(';'):
        return True
    # Setup new path value
    new_path_value_to_set = current_path_value
    if not new_path_value_to_set.endswith(';'):
        new_path_value_to_set += ';'
    new_path_value_to_set += _path
    # Set new path value
    p = subprocess.Popen(['powershell.exe', '[Environment]::SetEnvironmentVariable("PATH", "{0}", "User")'.format(new_path_value_to_set)], stdout=subprocess.PIPE, shell=True)
    p.wait()
    # Check that it was set
    new_path_value = get_path()
    return _path in new_path_value.split(';')


# Give information about what we know
print(INFO + 'This script is running on Python {0}.{1}.{2}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
print(INFO + 'The executable running this script is at: {0}'.format(sys.executable))
print(INFO + 'Python installation root is at: {0}'.format(sys.exec_prefix))
if sys.exec_prefix != sys.base_exec_prefix:
    print(WARN + 'It looks like you\'re using a virtualenv. We\'ll try to add the base Python version to make things easier.')
print('')

# Get current user path variable
path_variable = get_path()
path_variable_paths = [i for i in path_variable.split(';') if i != '']
print(INFO + 'Current user PATH variable contains:')
for path in path_variable_paths:
    print('\t{0}'.format(path))

# Check if the installation root is in the variable
if folder_path_in_path_variable(sys.base_exec_prefix, path_variable_paths):
    print(OK + 'Python installation root path is in the users PATH variable')
    base_path_addition_required = False
else:
    print(ACTION + 'Python installation root path is not in the users PATH variable')
    base_path_addition_required = True

# Check if the scripts folder is in the variable (first make sure it exists)
scripts_folder_location = sys.base_exec_prefix + '\\Scripts'
if os.path.isdir(scripts_folder_location):
    if scripts_folder_location in path_variable or scripts_folder_location + '\\' in path_variable:
        print(OK + 'Scripts folder path is in the users PATH variable')
        scripts_path_addition_required = False
    else:
        print(ACTION + 'Scripts folder path is not in the users PATH variable')
        scripts_path_addition_required = True
else:
    print(WARN + 'Cannot locate Scripts folder at {0}'.format(scripts_folder_location))
    scripts_path_addition_required = False

# If anything needs to be added, check with the user first
if base_path_addition_required or scripts_path_addition_required:
    answer = input('Do you want to add the required paths to the users path environment variable? ')
    # If they say yes, add the required paths
    if answer.lower() in ['yes', 'y']:
        changed = False
        print('')

        # Add the Python root
        if base_path_addition_required:
            if add_path(sys.base_exec_prefix):
                print(OK + 'Successfully added the Python installation root path to the users PATH variable')
                changed = True
            else:
                print(ERROR + 'Failed to add the Python installation root path to the users PATH variable')

        # Add the Scripts path
        if scripts_path_addition_required:
            if add_path(scripts_folder_location):
                print(OK + 'Successfully added the Scripts folder path to the users PATH variable')
                changed = True
            else:
                print(ERROR + 'Failed to add the Scripts folder path to the users PATH variable')

        # If anything was changed, notify the user they need to restart applications to get it
        if changed:
            print('')
            print(WARN + 'You will need to restart applications to get the new path variable value')
else:
    input(INFO + 'No action required')
```

You should now be able to execute `python` and `pip` in the terminal with no errors.

> Note that if you have more than one Python installation, this script will add paths corresponding to what installation you ran the script with.
