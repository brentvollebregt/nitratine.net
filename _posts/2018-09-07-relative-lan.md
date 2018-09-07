---
layout: post
title: "Relative Lan"
date: 2018-09-07
categories: Projects
tags: Python
description: "Host your local project files that are linked using relative references on your network. This makes it easy to test a site out on other devices on your network."
---

* content
{:toc}

Host your local project files that are linked using relative references on your network. This makes it easy to test a site out on other devices on your network. Passing this script a file will search for the project root, host a server based around this root and then open the file you passed in your browser.

{% include addGitHubRepoBadges.html content="brentvollebregt/relative-lan" %}

<!-- more -->

## Getting Started
### Prerequisites
 - Python 2.7 or 3+
 - No dependencies!

### Installing Via [GitHub](https://github.com/brentvollebregt/relative-lan)
```
$ git clone https://github.com/brentvollebregt/relative-lan.git
$ cd relative-lan
$ python setup.py install
```
Then to run it, execute the following in the terminal:
```
$ relative-lan index.html
```

Where index.html is a file in your web project with relative links to other local files.

### Running With No Instillation Via [Github](https://github.com/brentvollebregt/relative-lan)
Simply call:
```
> python relative_lan.py index.html
```

#### Arguments
| Argument | Description     |
|----------|-----------------|
| filename (positional) | Find the root using this file and open it when the server is started |
| -p       | Set the port for the server |
| -r       | Set the root directory manually for the server (can still pass a file to open) |
| -s       | Don't allow files outside of the root directory to be served |
| -d       | Disable the browser being opened when the script is called |
| -v       | Enable verbose mode (including server output) |

*You may leave the positional filename argument out if -r is set. In this case, no web-page will be opened as a file hasn't been provided.*

## How Does This Work?
Regarding you don't pass the root directory yourself, this script will search the file you passed for relative references. Files found will then be recursively searched to determine where the project root is.

Whenever a request is make to the server, the url will be converted into a relative reference from the root directory found/provided.
