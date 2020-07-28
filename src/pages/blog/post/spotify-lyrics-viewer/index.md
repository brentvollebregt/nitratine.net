---
templateKey: blog-post
title: "Spotify Lyrics Viewer"
date: 2019-11-07T00:00:00.000+12:00
category: Projects
tags: [spotify, react, typescript, javascript, express]
image: feature.png
description: "Spotify Lyrics Viewer is a tool that allows you to view the lyrics of the current playing song on Spotify by simply signing into Spotify."
githubRepository: brentvollebregt/spotify-lyrics-viewer
disableToc: false
hidden: false
---

<div align="center" style="padding: 20px 20px 40px 20px">
    <img src="./spotify-lyrics-viewer-banner.png" alt="Spotify Lyrics Viewer Banner" style="margin-bottom: 10px;">
    <p class="text-center">View the lyrics of the current playing Spotify song in your browser.</p>
    <a href="https://spotify-lyrics-viewer.nitratine.net/"><button class="btn btn-outline-secondary" type="button">🌐 Visit spotify-lyrics-viewer.nitratine.net →</button></a>
</div>

The Spotify Lyrics Viewer is a tool that allows you to view the lyrics of the current playing song on Spotify.

## How it Works

To do this, it first logs you into Spotify so it can see the current song playing. The title and artist are then used to try and find the lyrics on [GENIUS](https://genius.com/) and whatever lyrics matched the best are displayed.

The web app periodically checks if a new song is playing and if so, will request for the new lyrics.

> The lyrics returned may not be for the current playing song in some situations due to the lyrics not existing on GENIUS or the fact that the current playing songs title has some extra content to it aside from the actual title.

## Screenshot

Below is a screenshot of me logged in and a song playing. The lyrics have been retrieved and displayed.

![Spotify Lyrics Viewer showing lyrics](sample.png)
