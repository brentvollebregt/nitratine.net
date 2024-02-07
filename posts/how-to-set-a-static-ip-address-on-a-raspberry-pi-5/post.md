title: "How to Set a Static IP Address on a Raspberry Pi 5"
date: 2024-02-08
category: Tutorials
tags: [raspberry-pi, networking]
feature: feature.jpg
description: "This tutorial explains how to set a static IP address on a Raspberry Pi 5 using nmcli"

[TOC]

## Your Pi

Ideally you already have your Raspberry Pi set up and connected to a network that has assigned you an IP address using DHCP. In my case, the network I will be modifying was set up when I imaged the Raspberry Pi OS to my SD card (the Wi-Fi connection).

## nmcli vs. dhcpcd

A lot of tutorials you may find for setting a static IP address on a Raspberry Pi will mention dhcpcd. As [discussed here](https://raspberrypi.stackexchange.com/questions/144886/how-to-set-up-a-static-ip-on-raspberry-pi-5-with-raspbian-dhcpcd-conf-missing), dhcpcd was replaced with nmcli in the newer releases.

## Setting the Static IP

First, we need to find the name of the configuration to update. Run `nmcli con show` to show all connections, this will output something like this:

```
NAME                UUID                                  TYPE      DEVICE
preconfigured       5ec704b5-ca57-4c37-9426-6639dbb3a1ff  wifi      wlan0
lo                  5074d0fb-5b49-4f91-bb3b-1835a64f0a77  loopback  lo
Wired connection 1  6aa86725-6e8b-4b1f-94b5-3401e4c7eb27  ethernet  eth0
```

I want to update the configuration associated with Wi-Fi which is device wlan0 - this means the configuration I need to update is "preconfigured".

Next set the the IPv4 address, you will need to substitute your configuration name and IPv4 address in CIDR notation in this command: `nmcli con mod <configuration name> ipv4.addresses <ip address>`. So I would run,

```text
nmcli con mod preconfigured ipv4.addresses 192.168.1.100/24
```

Next set the IPv4 gateway, for a lot of people, this will be the IP address of your router,

```text
nmcli con mod preconfigured ipv4.gateway 192.168.1.1
```

Next set the DNS, again, you could use your router but you could also use another like `8.8.8.8`,

```text
nmcli con mod preconfigured ipv4.dns 8.8.8.8
```

Next set the addressing from DHCP to static,

```text
nmcli con mod preconfigured ipv4.method manual
```

Restart the connection to pick up these changes,

```text
nmcli con up preconfigured
```

Check your new IP address with `ip addr show wlan0` (or whatever device you are using). Lastly check your network connectivity by doing a quick ping using `ping 8.8.8.8`.

## Potential Issues

### My IP address changed but `ping 8.8.8.8` doesn't work

If you can see the Raspberry Pi has the new IP address but it cannot talk to the internet, you may have forgotten to set the DNS or have set it to something that isn't a DNS.

## Credits

- [Feature image](https://unsplash.com/photos/green-and-white-circuit-board-eaDwf4UAEhk)