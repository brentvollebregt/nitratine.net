---
layout: post
title: "Get WiFi Passwords With Python"
date: 2017-12-13
categories: Youtube
tags: Python WiFi
---

* content
{:toc}

This script searches windows for wifi passwords already known and displays them along side the network name. It will not find passwords that your computer doesn't already know. This is useful for the occasions that you forget your WiFi password.

{% include embedYouTube.html content="Z_QAvJ8sr6A" %}

> Unfortunately on the 7-5-2018 YouTube decided to give me a community guideline strike and has removed the video. I have appealed as it fell under "content that encourages illegal activities or incites users to violate YouTube's guidelines" which it is not; this is an educational video.

## Quick Background Idea
If you type ```netsh wlan show profiles``` in cmd, you will be shown the profiles for wifi connections your computer has stored.

If you then type ```netsh wlan show profile {Profile Name} key=clear```, the output provided will contain the network key which is the WiFi password.

<!-- more -->

## Getting the Passwords
First import subprocess, this is the module we will use to interact with the cmd.

```python
import subprocess
```

Next, get the output for the command "netsh wlan show profiles" using subprocess.check_output(). Then decode the output with utf-8 and split the string by a newline character to get each line in a separate string. 

```python
a = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
```

Now that we have a list of strings, we can get lines that only contain "All User Profile". With these lines we then need to split it by a ':', get the right hand side and remove the first and last character

```python
a = [i.split(":")[1][1:-1] for i in a if "All User Profile" in i]
```

Now that the variable a contains the WiFi profile names, we can get the output for the command "netsh wlan show profile {Profile Name} key=clear" using subprocess.check_output() again for a particular profile while looping through all profiles.

```python
for i in a:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
```

Still in the loop, find lines that contain "Key Content", split by ':' and remove the first and last character just like before

```python
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
```

Now we should have a list containing one string which is the particular profiles key. Here you could just use a simple print statement but I have just formatted it a bit.

```python
    try:
        print ("{:<30}|  {:<}".format(i, results[0]))
    except IndexError:
        print ("{:<30}|  {:<}".format(i, ""))
```

Now put a input call at the end of the script outside the loop so that when the script is run it will not immediately stop when results are displayed.

```python
a = input("")
```

Save this file with a .py extension and you can now run the script. You can run it by double clicking on the script, running it in IDLE or even cmd using ```python {filename}```.

## Final Script

```python
import subprocess

a = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
a = [i.split(":")[1][1:-1] for i in a if "All User Profile" in i]
for i in a:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    try:
        print ("{:<30}|  {:<}".format(i, results[0]))
    except IndexError:
        print ("{:<30}|  {:<}".format(i, ""))
a = input("")
```

You can also find the gist for this [on Github here](https://gist.github.com/brentvollebregt/30d278eae98e2ff221add008259d42bb).

## UnicodeDecodeError Ignoring - Revision 1
It has come to my attention that many people are having issues with this raising a UnicodeDecodeError describing that 'utf-8' codec can't decode a specific byte. This is caused by a byte in one of the profile names not being a character that is in the utf-8 encoding.

One way to fix this is changing the encodings from `utf-8` to `cp1252` or another coding which may support your character. **Do this first before trying the next script**

Another way is to ignore the error and catch it later on. So the new code in this case would be.

```python
import subprocess

a = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="ignore").split('\n')
a = [i.split(":")[1][1:-1] for i in a if "All User Profile" in i]
for i in a:
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="ignore").split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            print ("{:<30}|  {:<}".format(i, results[0]))
        except IndexError:
            print ("{:<30}|  {:<}".format(i, ""))
    except subprocess.CalledProcessError:
        print ("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
a = input("")
```

Please note that profiles which cause an error will still not provide a password as the encoding still isn't correct. You will have to find the password manually as shown at the top of this post.

## FAQ

### Why isn't the password showing for one or more network(s)?
If a network has a special type of authentication, there is a good chance this will not obtain the password. There will most likely be other methods of finding the password though.

*Please leave questions and comments related to the video on YouTube as they will be replied to faster there*
