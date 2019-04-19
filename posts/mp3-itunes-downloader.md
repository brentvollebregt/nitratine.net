title: "MP3-iTunes Downloader"
date: 2017-12-21
category: Projects
tags: [python, itunes, download, youtube-dl]
feature: gui1.png
description: "A Python script that allows a user to download a particular song from an iTunes-listed album. It uses YouTube as an audio source and iTunes to tag the mp3 file."

{% with repo="brentvollebregt/mp3-iTunes" %}{% include 'blog-post-addGitHubRepoBadges.html' %}{% endwith %}

## What is this?
This project allows you to select a song from an album found on the web version of iTunes and download it by sourcing the audio from YouTube and tags from iTunes.

## Demonstration and Screenshots
![GUI example](/post-assets/mp3-itunes-downloader/gui1.png)

## Requirements
* Python (tested with 3.5)
* ffmpeg (described in Installation steps 2+3)

## Setup
1. Clone this repository: `git clone https://github.com/brentvollebregt/mp3-iTunes.git`
2. cd into the directory: `cd mp3-iTunes`
3. Install the requirements: `pip install -r requirements.txt`
2. Go to [http://ffmpeg.zeranoe.com/builds/](http://ffmpeg.zeranoe.com/builds/) and download ffmpeg.
3. Extract the files and copy ffmpeg.exe, ffplay.exe abd ffprobe.exe from the /bin folder to the location of music_downloader_with_YT_iTunes.py *(you can also put these in a location that is reference by the PATH variable if you wish)*

## Usage
1. Go to the browser version of iTunes and find the album your desired song is in (e.g. [https://itunes.apple.com/nz/album/wolves/id1227716339](https://itunes.apple.com/nz/album/wolves/id1227716339) and copy the url.
2. Run music_downloader_with_YT_iTunes.py and insert the iTunes url and the number of the song in the album.
3. Click get data
4. Change tag details if needed
5. Click open search and copy a youtube url with good audio quality that has your desired song.
3. Click download. Files will be saved to output/ in the cwd.
