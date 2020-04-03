title: "Am I A Participant"
date: 2018-09-09
category: Projects
tags: [javascript, chrome-extension]
feature: feature.png
description: "Check if you are a participant of a conversation in Gmail. Helps you stop sending emails with the wrong address."

With this Chrome extension, a red outline around "Reply" and "Reply All" will appear if the currently logged in gmail account is not part of the conversation.

![Extension Popup](/posts/am-i-a-participant/buttons.png)

{% with repo="brentvollebregt/UoWMoodleIgnoreResourceWorkAround" %}{% include 'blog-post-addGitHubRepoBadges.html' %}{% endwith %}

## Installation
### Using the .crx File
1. Download the [.crx file](https://github.com/brentvollebregt/am-i-a-participant/raw/master/am-i-a-participant.crx)
2. Go to chrome://extensions/
3. Drag and drop the .crx file onto the extensions page
4. Click "Add extension"

> You will be notified that "*This extension is not listed in the Chrome Web Store and may have been added without your knowledge.*". This is because it has not been installed from the Chrome Web Store. If you are worried about this, you can use the method below.

### By Source
1. Download or clone the [repository](https://github.com/brentvollebregt/am-i-a-participant)
2. Go to chrome://extensions/
3. Turn developer mode on using the switch in the upper right
4. Click "*Load unpacked*" on the top left and select the *src* folder from the downloaded/cloned repository

## How Does This Work
Initially this script will wait for Gmails single-page-app to update the DOM (hopefully) and then get the emails that are used in the current conversation. These emails are then compared to the current email logged in and this used to determine if a warning is needed.
