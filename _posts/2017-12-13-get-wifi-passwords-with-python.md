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

## Quick Background Idea
If you type ```netsh wlan show profiles``` in cmd, you will be shown the profiles for wifi connections your computer has stored.

If you then type ```netsh wlan show profile {Profile Name} key=clear```, the output provided will contain the network key which is the WiFi password.

<!-- more -->

<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-6407227183932047"
     data-ad-slot="5275109384"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

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

## FAQ

### Why isn't the password showing for one or more network(s)?
If a network has a special type of authentication, there is a good chance this will not obtain the password. There will most likely be other methods of finding the password though.

*Please leave questions and comments related to the video on YouTube as they will be replied to faster there*
