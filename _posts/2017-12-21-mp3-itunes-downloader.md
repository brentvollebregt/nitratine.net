---
layout: post
title: "MP3-iTunes Downloader"
date: 2017-12-21
categories: Projects
tags: Python iTunes Download youtube-dl
description: "A Python script that allows a user to download a particular song from an iTunes-listed album. It uses YouTube as an audio source and iTunes to tag the mp3 file."
---

* content
{:toc}

A Python script that allows a user to download a particular song from an iTunes-listed album. It uses YouTube as an audio source and iTunes to tag the mp3 file.

[Find the project on GitHub here](https://github.com/brentvollebregt/mp3-iTunes)

## What is this?
This project allows you to select a song from an album found on the web version of iTunes and download it by sourcing the audio from YouTube and tags from iTunes.

## Demonstration and Screenshots
![GUI example](/images/mp3-itunes-downloader/gui1.png)

<!-- more -->

## Installation and Setup
1. Install Python (tested with 3.5)
2. Install requirements
    - mutagen (```pip install mutagen```)
    - youtube-dl (```pip install youtube-dl```)
    - BeautifulSoup4 (```pip install beautifulsoup4```)
    - PYQT5 (```pip install pyqt5```)
3. Get ffmpeg
    - Download ffmpeg from [http://ffmpeg.zeranoe.com/builds/](http://ffmpeg.zeranoe.com/builds/)
    - Extract the files and copy ffmpeg.exe, ffplay.exe and ffprobe.exe from the /bin folder to the location of spotify_album_downloader.py

## Usage
1. Go to the browser version of iTunes and find the album your desired song is in (e.g. [https://itunes.apple.com/nz/album/wolves/id1227716339](https://itunes.apple.com/nz/album/wolves/id1227716339) and copy the url.
2. Run spotify_album_downloader.py and insert the iTunes url and the number of the song in the album.
3. Click get data
4. Change tag details if needed
5. Click open search and copy a youtube url with good audio quality that has your desired song.
6. Click download. Files will be saved to /output/ in the current working directory.

