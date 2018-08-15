---
layout: page
disable_ads: true
title: About
permalink: /about/
icon: user-circle
type: page
description: "I am currently studying a Bachelor of Computing and Mathematical Sciences at the University of Waikato and plan to finish my 4th year in 2020. I started learning Python by myself back in 2013 and have learnt all the Python I know myself and most of the CSS/HTML/JavaScript myself."
---

* content
{:toc}

I am currently studying a Bachelor of Computing and Mathematical Sciences at the University of Waikato and plan to finish my 4th year in 2020.

I started learning Python by myself back in 2013 (I was year 10) and have learnt all the Python I know myself and most of the CSS/HTML/JavaScript I know myself. In University I clicked onto other languages fast and I have had the opportunity to use a variety of languages and frameworks.

Find me on other platforms:
<ul>
    <li><a href="https://github.com/brentvollebregt"><i class="fa fa-github" aria-hidden="true"></i> Github</a></li>
    <li><a href="https://www.youtube.com/PyTutorialsOriginal"><i class="fa fa-youtube" aria-hidden="true"></i> YouTube</a></li>
    <li><a href="https://stackoverflow.com/users/3774244/brent-vollebregt"><i class="fa fa-stack-overflow" aria-hidden="true"></i> Stackoverflow</a></li>
</ul>

## Projects
This is a small list of my favourite projects I have developed.

### [Auto Py To Exe]({{ site.baseurl }}{% link _posts/2018-03-10-auto-py-to-exe.md %})
This is the project I am most proud of to date. I wanted to fix the problem of converting (packaging) Python to a windows executable to run on computers without python installed being a confusing job for new-comers.

This project allows someone to easily set up a server that uses chromes app mode as an interface and then calls pyinstaller with the parameters provided by the user.

<div style="text-align: center">
	<img src="https://i.imgur.com/EuUlayC.png" alt="Empty interface"/>
</div>

I uploaded this project to [PyPI](https://pypi.org/project/auto-py-to-exe/) so it can be installed using:
```
$ python -m pip install auto-py-to-exe
```
and then run using:
```
$ auto-py-to-exe
```

### [PyTutorials YouTube Channel](https://www.youtube.com/PyTutorialsOriginal)
![Channel Header]({{ site.baseurl }}{% link images/PyTutorials-channel-header.jpg %})
When I have time and ideas, I like to make programming tutorials. Currently most of my tutorials are Python related but I also have a few different ones.

Some of my videos have quite a bit of attention, for example [Convert PY to EXE](https://youtu.be/lOIJIk_maO4) which has over 210k views, [Python Keylogger](https://youtu.be/x8GbWt56TlY) with more tha 110k views and [Record Your Computer Screen With VLC](https://youtu.be/H-6gxvBBEiw) with more than 790k views.

I give a lot of help in the comments for these videos and try my best to find solutions for issues people are having. This also allows me to gauge what people like in terms of topics and the videos themselves and get great feedback.

### [Price Per Unit]({{ site.baseurl }}{% link _posts/2018-06-28-price-per-unit.md %})
![Price Per Unit Header]({{ site.baseurl }}{% link images/price-per-unit/FeatureGraphic.jpg %})
This project is an Android app that compares prices for similar items and will calculate the price per unit for each item. These values can then be compared to find the best value for money. Simply give a name (optional), enter in the cost, amount and size of each item and the unit per dollar will be calculated.

### [Multi Clipboard]({{ site.baseurl }}{% link _posts/2018-08-15-multi-clipboard.md %})
This project fixed my issue of having to re-copy something after I just overwrote my clipboard with something else.

It does this by opening a simple GUI that allows you to have temporary clipboards like a hotbar. You simply attach the script to a hotkey and when called, select which clipboard you want to use and whatever was in that virtual clipboard will now be in your actual clipboard. It also allows you to add and delete virtual clipboards.

<div style="text-align: center">
	<img src="{{ site.baseurl }}{% link images/multi-clipboard/main-gui-with-settings-shown.png %}" alt="Multi Clipboard GUI"/>
</div>

### [Quick Script]({{ site.baseurl }}{% link _posts/2017-12-20-quick-script.md %})
This project allowed me to have a lot of small scripts in one place that is easy to get to.

Just like Multi Clipboard, attach this to a hotkey and your scripts you previously added (tutorial in README) will appear. Example scripts come pre-loaded like saving a clipboard image to a file, restarting windows explorer and putting your ip address on your clipboard.

<div style="text-align: center">
	<img src="{{ site.baseurl }}{% link images/quick-script/gui1.png %}" alt="Quick Script GUI"/>
</div>

### [Nitratine](http://nitratine.pythonanywhere.com/)
Nitratine was a website I built before this site to host all my content.

It is a fully dynamic server with a cms built in. It can do server side scripting, uses Jinja for templating, has mobile support and more.

I no longer use it as I felt a static site was much more suitable and easier to maintain. I still get a bit of traffic to it each day though.

![Desktop home split light dark snow]({{ site.baseurl }}{% link images/the-nitratine-project/nitratine1.jpg %})

### [Colour]({{ site.baseurl }}{% link _posts/2017-11-18-colour.md %})
This was an app that I had made as a joke with a neighbour. It demonstrates how something simple can take so long to complete.

The aim of this app is to collect all the colours by simply tapping the screen to get a colour. The trick is that each time you tap the screen, one of the 16,777,216 possible colours to display are generated randomly; thus making it a very long trip to finish the apps purpose.

I did some math and testing [here]({{ site.baseurl }}{% link _posts/2017-12-07-randomly-generating-numbers-to-fulfil-an-integer-range.md %}) and guessed (based off calculations) it would take about 134 and a half years to finish the app if you tapped then screen at a rate of 400 taps per minute.

<div style="text-align: center">
	<img style="width: 30%; display: inline;" src="{{ site.baseurl }}{% link images/colour/tap-screen.png %}" alt="Main screen"/>
	<img style="width: 30%; display: inline;" src="{{ site.baseurl }}{% link images/colour/colour-viewer.png %}" alt="Colour finder"/>
	<img style="width: 30%; display: inline;" src="{{ site.baseurl }}{% link images/colour/colour-mixer.png %}" alt="Colour mixer"/>
</div>

## Some Technologies I Have Worked With
<div style="text-align: center">
    <!-- Python -->
    <img src="{{ site.baseurl }}/images/icons/python.svg" title="Python" alt="Python" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- Java -->
    <img src="{{ site.baseurl }}/images/icons/java.svg" title="Java" alt="Java" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- JavaScript -->
    <img src="{{ site.baseurl }}/images/icons/javascript.svg" title="JavaScript" alt="JavaScript" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- Clojure -->
    <img src="{{ site.baseurl }}/images/icons/clojure.svg" title="Clojure" alt="Clojure" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- HTML -->
    <img src="{{ site.baseurl }}/images/icons/html.svg" title="HTML" alt="HTML" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- CSS -->
    <img src="{{ site.baseurl }}/images/icons/css.svg" title="CSS" alt="CSS" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- SQLite -->
    <img src="{{ site.baseurl }}/images/icons/sqlite.svg" title="SQLite" alt="SQLite" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- Android -->
    <img src="{{ site.baseurl }}/images/icons/android.svg" title="Android" alt="Android" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- Flask -->
    <img src="{{ site.baseurl }}/images/icons/flask.svg" title="Flask" alt="Flask" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- Git -->
    <img src="{{ site.baseurl }}/images/icons/git.svg" title="Git" alt="Git" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- JetBrains -->
    <img src="{{ site.baseurl }}/images/icons/jetbrains.svg" title="JetBrains" alt="JetBrains" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- Linux -->
    <img src="{{ site.baseurl }}/images/icons/linux.svg" title="Linux" alt="Linux" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- PhotoShop -->
    <img src="{{ site.baseurl }}/images/icons/photoshop.svg" title="Adobe PhotoShop" alt="Adobe PhotoShop" style="width: 80px; margin: 0 5px; display: inline;">
    <!-- C# -->
    <img src="{{ site.baseurl }}/images/icons/csharp.svg" title="C#" alt="C#" style="width: 80px; margin: 0 5px; display: inline;">
</div>

## Contact
Please leave questions about videos on YouTube and blog posts in the comments at the bottom of the post. Emails regarding this nature will be referred back to the corresponding platform.

If you would like to contact me for another reason, send an email to <a id="email" href="javascript:displayEmail();">[Display Email Address]</a>

<script>
function displayEmail() {
    alert("Please leave questions about videos on YouTube and blog posts in the comments at the bottom of the post.");
    document.getElementById('email').innerHTML = "{{ site.email }}";
    document.getElementById('email').href = "mailto:{{ site.email }}";
}
</script>
