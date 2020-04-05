title: "University of Waikato Moodle Resource Work Around Ignorer"
date: 2018-09-08
category: Projects
tags: [javascript, chrome-extension]
feature: target.png
description: "A chrome extension to solve the Waikato Universities resource work around in Moodle."
github: brentvollebregt/uow-moodle-rwa-ignorer

Simply install this extension in Google Chrome and safely open documents in Moodle in a new tab without wanting to rip your hair out.

![Extension Popup](/posts/uow-moodle-rwa-ignorer/extension-popup.png)

## Installation
### Using the .crx File
1. Download the [.crx file](https://github.com/brentvollebregt/uow-moodle-rwa-ignorer/raw/master/uow-moodle-rwa-ignorer.crx)
2. Go to chrome://extensions/
3. Drag and drop the .crx file onto the extensions page
4. Click "Add extension"

> You will be notified that "*This extension is not listed in the Chrome Web Store and may have been added without your knowledge.*". This is because it has not been installed from the Chrome Web Store. If you are worried about this, you can use the method below.

### By Source
1. Download or clone the [repository](https://github.com/brentvollebregt/uow-moodle-rwa-ignorer)
2. Go to chrome://extensions/
3. Turn developer mode on using the switch in the upper right
4. Click "*Load unpacked*" on the top left and select the *src* folder from the downloaded/cloned repository

## What Actually is This?
If you are a student of the University of Waikato and have tried to use "Open in new tab" on particular files in moodle, there is a chance you will be greeted with this amazing page:

![Extension Popup](/posts/uow-moodle-rwa-ignorer/target.png)

It gets pretty annoying and it's quite unpredictable when it will occur. This chrome extension will look at pages where urls match a pattern and search for the `resourceworkaround` class. If found, it will redirect the user to the actual file.
