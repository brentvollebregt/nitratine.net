---
templateKey: blog-post
title: "How to get Stored WiFi Passwords in Windows"
date: 2020-05-12T12:00:00.000Z
category: Tutorials
tags: [wifi]
image: feature.png
description: "This tutorial describes how to identify stored WiFi passwords in Windows using the command prompt. This is very helpful for identifying your forgotten WiFi passwords."
hidden: false
---

[TOC]

A while ago I made a tutorial on [Getting WiFi Passwords With Python](/blog/post/get-wifi-passwords-with-python/) which provides a script that automates the following process. For those that don't want to install Python, this is how to identify stored WiFi passwords manually.

## Identifying the Target Profile
First, you need to identify the profile associated with the stored WiFi connection. To do this, open the command prompt and execute the following.

```bash
netsh wlan show profiles
```

You should get an output that looks something like this:

```text
User profiles
-------------
    All User Profile     : WiFi Network 1
    All User Profile     : WiFi Network 2
    All User Profile     : WiFi Network 3
    All User Profile     : WiFi Network 4
    All User Profile     : WiFi Network 5
    All User Profile     : Other WiFi Network 6
    All User Profile     : Yet another WiFi Network 7
```

This output shows the associated profile for each of your stored WiFi connections. Copy or remember the exact text of the profile, e.g. `WiFi Network 2` as it will be used in the next step.

> If your WiFi SSID/name is not in this list, you will not be able to identify the password as it is not a stored connection.

## Obtaining the Profile's Password
In cmd again, execute the following after replacing the profile name:

```bash
netsh wlan show profile "<profile name>" key=clear
```

For me, I would execute `netsh wlan show profile "WiFi Network 2" key=clear` as I am looking for the password associated with the profile `WiFi Network 2`.

This will output some information about the network, if you go down to *Security settings* and look beside *Key Content*, you will see your WiFi password.

```text
Security settings
-----------------
    Authentication         : WPA2-Personal
    Cipher                 : CCMP
    Authentication         : WPA2-Personal
    Cipher                 : GCMP
    Security key           : Present
    Key Content            : yourpassword!   <-- here is the WiFi password
```
