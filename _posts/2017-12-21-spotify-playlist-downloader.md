---
layout: post
title: "Spotify Playlist Downloader"
date: 2017-12-21
categories: Projects
tags: Python Spotify Download youtube-dl
description: "A python script to download a Spotify playlist to MP3 using YouTube as audio source. The MP3s are tagged and given album art using Spotify"
---

* content
{:toc}

A python script to download a Spotify playlist to MP3 using YouTube as audio source. The MP3s are tagged and given album art using Spotify

{% include addGitHubRepoBadges.html content="brentvollebregt/spotify-playlist-downloader" %}

## What is this?
This project takes a Spotify playlist uri and will download it's contents by sourcing audio from YouTube and tags/art from Spotify. YouTube videos for audio are found automatically.

## Demonstration and Screenshots
![Console example](/images/spotify-playlist-downloader/gui1.png)

This is a console application, simply paste the uri and press enter.

<!-- more -->

## Installation and Setup
1. Install Python (tested with 3.5)
2. Install requirements
    - mutagen (pip install mutagen)
    - youtube-dl (pip install youtube-dl)
    - BeautifulSoup4 (pip install beautifulsoup4)
3. Get ffmpeg
    - Download ffmpeg from [http://ffmpeg.zeranoe.com/builds/](http://ffmpeg.zeranoe.com/builds/)
    - Extract the files and copy ffmpeg.exe, ffplay.exe and ffprobe.exe from the /bin folder to the location of spotify_album_downloader.py
4. Go to [https://developer.spotify.com/my-applications](https://developer.spotify.com/my-applications) and create an app to get a client_id and client_secret key pair
5. Put these keys in settings.json

## Usage
1. Get the URI of a spotify playlist by sharing it and clicking URI on the far right. This will copy the URI to your clipboard.
2. Run spotify_album_downloader.py and insert your Spotify URI, then hit enter.
3. Files will be saved to /output/ in the current working directory.
4. The script will say when it is complete, press enter to close.

## Notes
This project uses the Spotipy module which was sourced from [https://github.com/plamere/spotipy](https://github.com/plamere/spotipy)
