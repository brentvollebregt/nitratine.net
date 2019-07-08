title: "Emotionify"
date: 2019-07-09
category: Apps
tags: [react, javascript, spotify]
feature: feature.png
description: "Emotionify is a webapp that allows users to login to Spotify, select a playlist and then sort them using Spotify's pre-calculated audio feature values."

[TOC]

<div align="center" style="padding: 20px 20px 40px 20px">
    <img src="/post-assets/emotionify/emotionify-banner.png" alt="Emotionify Banner">
</div>

## What is This?
Emotionfy is a webapp that allows users to easily sort their playlists using Spotify's pre-calculated audio feature values. By default, this project aims to create emotionally gradiented Spotify playlists for smoother emotional transitions. It does this by sorting songs based off the two features `Valence` and `Energy` [calculated by Spotify](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) based on distance from the origin.

Users have the option to change what songs are sorted by and how they are sorted. It is also possible to select more than one playlist when sorting songs. Below is a visualisation of one of my playlists being sorted:

![Example Visulisation Sort of a Personal Playlist](/post-assets/emotionify/emotionify-sort-comparison.png)


## The Future of Emotionify
I plan to eventually add features that allow users to look at an overview of their playlist's audio features and relations as well as add "playlist utilities" to help making more detailed playlists.

> Currently the source is not being released as early development occurs.
