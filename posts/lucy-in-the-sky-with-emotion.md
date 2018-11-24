title: "Lucy In The Sky With Emotion"
date: 2017-12-21
category: Projects
tags: [Python, Machine-Learning]
feature: visualiser5.jpg
description: "This project aimed to visualise emotion in music with software developed by six people from the COMP241 (Software Engineering Development) paper as a group project. The project was successful in the end using Spotify to assist emotion detection."

[TOC]

{% with repo="shash678/Lucy-In-The-Sky-With-Emotion" %}{% include 'blog-post-addGitHubRepoBadges.html' %}{% endwith %}

## What is this?
This project takes a local library of music that is tagged and will predict the emotion of the song of either happy or sad. This data can then be passed to a visualiser which will play the selected song along with fiv other recommended songs based off it's emotional position on a valence energy plane.

When the project is first started it will create a sklearn.neighbors.KNeighborsClassifier instance and be provided [previously researched data]({{ url_for('blog_post', path='finding-emotion-in-music-with-python') }}) for points to be compared to later. The Browse button then needs to be clicked and a directory selected. The music library is then scraped for tags and searches for them in Spotify. We then get audio data from Spotify for each song (if possible) and present the data on the GUI. When a user clicks on a song, recommendations of the five nearest songs based off emotion, song data and the point on the emotion gradient are all displayed to the user. When the user clicks the Visualise button, data will be sent to the visualiser and started.

## Demonstration and Screenshots
### GUI - Emotion Detection
![Emotion detection - Lucy in the sky with diamonds](/post-assets/lucy-in-the-sky-with-emotion/gui1.png)
![Emotion detection - All Star](/post-assets/lucy-in-the-sky-with-emotion/gui2.png)

### GUI - Valence Energy Graph
![GUI - Valence Energy Graph](/post-assets/lucy-in-the-sky-with-emotion/valence-plot.png)

### Visualiser
![Visualiser control](/post-assets/lucy-in-the-sky-with-emotion/visualiser1.jpg)
![Visualiser balls flying](/post-assets/lucy-in-the-sky-with-emotion/visualiser2.jpg)
![Visualiser environment view](/post-assets/lucy-in-the-sky-with-emotion/visualiser3.jpg)
![Visualiser paused](/post-assets/lucy-in-the-sky-with-emotion/visualiser4.jpg)
![Visualiser balls flying colse](/post-assets/lucy-in-the-sky-with-emotion/visualiser5.jpg)

### Installation and Setup
1. First clone the repository at [https://github.com/shash678/Lucy-In-The-Sky-With-Emotion](https://github.com/shash678/Lucy-In-The-Sky-With-Emotion)
2. Install Python (tested with 3.5.2)
3. If using Windows, run install_dependencies.bat. If not using windows, run the pip commands in the bat file. This will install most of the modules.
4. Install scipy by first dowloading it at [http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy) and then running ```pip install [file]```
5. Install numpy+mkl by first dowloading it at [http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy) and then running ```pip install [file]```
6. Build the visualiser using Unity
7. Edit the paths in main.py to link to the visualiser
    - Lines 123 and 125 to the locations of the desired output (123 for song files and 125 for the CSV file)
    - Line 156 to the executable to star the visualiser
8. Read about the issues below
9. Run main.py

#### Issues
Currently the visualiser cannot take in dynamic input for audio. CSV files are still read in dynamically and will change based on what song is selected when the visualise button is clicked.

This means music that was used in the building of the visualiser will be the only audio that the vislaiser plays, however the data that the visualiser reads from the CSV to manipulate some functions will still be used.

To temporarily fix this so incorrect data is not displayed can be easily fixed by commenting out lines 153 to 155 in main.py. This will disable the CSV wrting so the original CSV file will still be passing the correct data.

### Usage
To start this project, open up the emotion recognition part of the project by running main.py with Python. When the GUI appears, click Browse and select a folder that contains .mp3 tagged files (doesn't have to be in the top directory).

The Graph button can be pressed to display the songs on the emotion plane (Energy vs Valence).

After you have selected a song you want to visualise, click the Visualise button. After a short moment the visualiser will open and you will be promoted how you want to run it (speed and resolution).

When the visualiser has started, you can hold the left control key to display a list of the controls. These controls are:

- Esc - Pause
- Space - Freeroam the environment. Moves the ball off the pre defined path.
- Left / Right Arrows - Previous / Next Song
- C - Change Camera
- Z - Reset Balls
- X - Blow balls away from camera
- V - Change mood (for testing)

### Credits
#### Developers
- [Rhys Compton](https://github.com/basedrhys)
- [Dylan Exton](https://github.com/DylanExton)
- [Ryan Le Quesne](https://github.com/ryancomp241)
- [Seattle Tupuhi](https://github.com/minionsattle)
- [Brent Vollebregt](https://github.com/brentvollebregt)
- [Jack Woods](https://github.com/Woodsy1FD)

#### Project Managers
- [Swikrit Khanal](https://github.com/swikrit)
- [Sash Sinha](https://github.com/shash678)