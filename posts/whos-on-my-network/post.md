title: "Who's On My Network"
date: 2020-04-04
category: Projects
tags: [python, react, typescript, sqlite, networking]
feature: feature.png
description: "This tool helps you keep an eye on who is on your network and when. Simply periodically scan your network, assign devices to people and view who is on your network."
github: brentvollebregt/whos-on-my-network

[TOC]

<div align="center" style="padding: 20px 20px 40px 20px">
    <img src="/posts/whos-on-my-network/whos-on-my-network-logo.png" alt="Who's On My Network Logo" style="margin-bottom: 10px;">
    <p class="text-center">Keep an eye on who is on your network and when.</p>
</div>

Who's On My Network is a tool built-in Python with a React interface that allows you to scan your network to observe who's on it currently and look at past scans to see who was on it previously.

![Who's On My Network Overview Demo](/posts/whos-on-my-network/overview-screenshot.png)

*This screenshot shows an overview of scans done between two dates and which devices were detected.*

## What This Tool Does
This application does two primary tasks; scanning a network and displaying data.

The Python module is capable of scanning once or scanning repetitively. This is done by executing a basic command in a terminal.

All scans can then be identified in the interface where a user can create profiles for each person they know is on the network and assign discovered devices to people. This helps identify devices you do not know about and unusual connections.

## Getting the Tool Yourself

Details in the [projects README](https://github.com/brentvollebregt/whos-on-my-network#readme) outline how to download and setup the tool.

The tool offers help for:

- Docker compose (build hosted on GitHub)
- Docker compose with a local build
- Bare metal


## Using The Tool
The tool is built around a Python module that can be run using `python -m whos_on_my_network <arguments>` or simply executing `python run.py <arguments>`.

> See [README.md in the git repository](https://github.com/brentvollebregt/whos-on-my-network#%EF%B8%8F-usage) for details about arguments.

### Scanning Your Network
To scan the network once, you can use `python -m whos_on_my_network current`. This will output a table displaying the MAC address, IP address and hostname of all detected devices. This data has also been saved to the database to be viewed later.

To scan the network repetitively, you can use `python -m whos_on_my_network watch`. This will scan the network every 5 minutes (by default - can be changed) repeatedly unless told to only scan a specific amount of times. Each scan will also be saved to the database to be viewed later.

### Viewing Scans and Creating Associations
Execute `python -m whos_on_my_network start` and go to `localhost:8080` in your browser. You can now view scans and create associations between devices and people.

> Note: Text substitution has been done in these screenshots below so connections may not add up; this is not the tool. 

#### Scans
![Who's On My Network Scan Screenshot](/posts/whos-on-my-network/scans-screenshot.png)

The scans page shows scans that have been made.

On the scans page, you can select a date range and view all the scans in that period. When clicking on a scan (row on the table), you will be directed to more focused data on that scan, in particular, showing the time, network id used and details about each device.

![Who's On My Network Scan Screenshot](/posts/whos-on-my-network/scan-screenshot.png)

### Devices
![Who's On My Network Devices Screenshot](/posts/whos-on-my-network/devices-screenshot.png)

The devices page shows all devices that have been detected from scans.

On the devices page, you can filter by a text search, a particular owner or primary status. When clicking on a device (row on the table), you will be directed to more focused data on that device in particular.

![Who's On My Network Scan Screenshot](/posts/whos-on-my-network/device-screenshot.png)

> A primary device is a user-defined field that can signify whether the device is always on the person or not - so it could be used to identify when near or not.

### People
![Who's On My Network People Screenshot](/posts/whos-on-my-network/people-screenshot.png)

The people page shows people that have been created by the user of this tool

On the people page, you can filter by a text search to find a particular person. When clicking on a person (row on the table), you will be directed to more focused data on that person in particular.

![Who's On My Network Scan Screenshot](/posts/whos-on-my-network/person-screenshot.png)

### Current
Another page is also supplied that allows you to run a single scan from the browser without having to run the scan command.

## How This Tool Works
By default, this tool uses [scapy](https://scapy.net/) to send ARP packets to all addresses in the provided network range (default is 192.168.1.0/24) to identify what devices are on the network. When a host responds, its MAC address, IP address and hostname are obtained and an entry is added to the SQLite database matched to the current scan.

Custom scanners are supported by this application to allow custom methods of identifying devices on a network. An example has been provided for WiFi networks that use a [ASUS RT-AC58 router](https://github.com/brentvollebregt/whos-on-my-network/blob/master/whos_on_my_network/scanners/asus_rt_ac58u.py). This scanner demonstrates how you can instead look at the active devices connected to your router rather than scanning the network.

All data collected by the application is stored locally in an SQLite database.
