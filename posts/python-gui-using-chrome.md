title: "Python GUI Using Chrome"
date: 2018-05-05
categories: YouTube
tags: [Python, GUI, Chrome, JavaScript]
feature: feature.png
description: "Eel is a little Python library for making simple Electron-like HTML/JS GUI apps. This used for creating GUI's in a Chrome app window with HTML, CSS and JS. In summary it hosts a local webserver, then provides features to communicate between JavaScript and Python."

[TOC]

When thinking of what to design [auto-py-to-exe]({{ url_for('blog_post', path='auto-py-to-exe') }}) with, I came across [Eel](https://github.com/ChrisKnott/Eel) for creating GUI's using HTML, CSS and JavaScript in a Chrome app window. Hosting a local webserver and using Chromes app mode was exactly what I needed to make this project look great. Also this library ets you annotate functions in Python so that they can be called from Javascript, and vice versa.

{% with video_id="2kbeBzEQfXE" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}

> Please note that this content is based off README.md in [Eel's GitHub Repository](https://github.com/ChrisKnott/Eel) with modifications.

## Setup
To use Eel you will need to install the library by simply calling `pip install eel` in cmd. Make sure no errors occurred and if you don't have pip head over to [how-to-setup-pythons-pip]({{ url_for('blog_post', path='how-to-setup-pythons-pip') }}). To make sure Eel is installed, open IDLE and execute `import eel`. If no errors appear then it has installed properly.

Although this example will be displaying the use of chromes app mode, you do not actually need [chrome](https://www.google.com/chrome/). When starting the app, if you do not have chrome you will be asked what to open to display the webpage.

## Creating the File Structure
When setting up your file structure, the files to be served to the chrome window need to be in a single directory. In this example I will be putting my file in the `web/` directory; you can use a different folder name if you want.

```console
server.py         <-- Python scripts
another_module.py
web/              <-- Web folder
  main.html
  css/
    style.css
  img/
    logo.png
  js/
    myscript.js
```

Python files will still sit outside the web/ folder and I recommend that you put the web/ folder right beside your python script to make it easier to reference when setting up the server. You can split the web/ folder into further folders if you want but this is not required.

## Creating the App
The simplest form of creating this app is three lines:

```python
import eel
eel.init('web')
eel.start('main.html')
```

This example imports eel, says where you files are and then starts the server passing the index page (page to display). When running the script, a chrome in app mode will appear and render the filename you passed in eel.start(). Chrome app mode is the same as chrome with the URL and bookmarks bar hidden.

If you do not have chrome installed, you will be asked what browser to open. The only difference when using this method is that you cannot control the initial size of the window.

![Hello World](/post-assets/python-gui-using-chrome/hello-world.png)

### App Options
You can set some optional variables when staring the server. To do this, pass a dictionary object to assigned to options as an argument; for example:

```python
my_options = {
	'mode': "chrome", #or "chrome-app",
	'host': 'localhost',
	'port': 8080,
	'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
}

eel.start('main.html', options=my_options)
```

In this example I have set 'mode' to 'chrome', this will mean that it will use chrome normally and not in app mode; use "chrome-app" to keep app mode (this is default). I set the 'host' to 'localhost' which will then host the server on 127.0.0.1. You could change this to your computers ip on your network so others can access the server. I have also set the port which is useful for clashes between servers and added chrome flags. Chrome flags are appended when calling the executable as usual.

*Remember that you do not have to pass all these options in the dictionary, you can pass one if you want.*

### Setting Window Size
If you are using chrome in app mode (default) you can specify the size of the window by passing a tuple to the size argument in eel.start(). For example:

```python
eel.start('main.html', size=(650, 612))
```

When I have used this in the past, the size doesn't always match up, a good example of this is in my [auto-py-to-exe]({{ url_for('blog_post', path='auto-py-to-exe') }}) project which uses `size=(650, 612)` but renders the window about 636x605. When looking at the inner dimensions of the window using JavaScript; window.innerHeight returns 573 and window.innerWidth returns 634.

This shows you might have to play around with these values until you get them where you want but they do work (just not as expected).

## Communication
Before you carry on, you will need to put a JavaScript file in your html file. Simply add to the header:

```html
<script type="text/javascript" src="/eel.js"></script>
```

This will allow JavaScript and Python to communicate as the client now has the code needed. There is nothing else you need to do apart from creating your functions.

## Making Python Functions you Can Call in JavaScript
To make a Python function that you can call from JavaScript decorate it with `@eel.expose` like this:

```python
@eel.expose
def my_python_method(param1, param2):
    print (param1 + param2)
```

Now when you call `eel.my_python_method('Hello ', 'world!');` in JavaScript, Python will print "Hello World!". This shows that the code is executed in the python instance, not in the chrome window; remember that - you cannot run Python code in JavaScript. You can however return data from Python back to JavaScript; I will describe this later.

## Making JavaScript Functions you Can Call in Python
To make a JavaScript function that you can call from Python wrap the function name in `eel.expose` before creating it like this:

```javascript
eel.expose(my_javascript_function);
function my_javascript_function(a, b) {
  console.log(a + b)
}
```

Now when you call `eel.my_javascript_function('Hello ', 'world!')` in Python, it will print "Hello World!" in the browsers console. This shows that the code was execute in JavaScript by calling the method in Python.

## Returning Values
Even though it may seem like Python and JavaScript are working together, there is still a barrier between them as they are running in different processes. Eel supports two ways to return values; callbacks and synchronous returns.

It's also good to note that passing complex objects between Python and JavaScript may not be possible due to the functions moving the data and the compatibility of the two languages for example you can't pass an instance of a class from Python to JavaScript.

### Callbacks
Callbacks allow us to execute a function with the data returned as the argument. When the data is returned, the function will be called and the return value will be passed as a parameter to the function. This method works both ways.

If I wanted to use a callback in Python, I would create my method in JavaScript which returns a value that is exposed using eel. Then in Python:

```python
def print_return(n):
    print('Return from Javascript: ', n)

# Call Javascript function, and pass explicit callback function
eel.js_function()(print_return)
```

This example will call js_function() in JavaScript and will pass the returned value to print_num() in Python.

You can also do this in JavaScript the other way around. For example:

```javascript
function print_return(n) {
    console.log(n)
}

eel.python_function()(print_return);
```

### Synchronous Returns
When calling a JavaScript function from Python, we can get the return value directly using a double pair of brackets; for example:

```python
return_value = eel.js_random()()  # This immeadiately returns the value
print('Got this from Javascript: ', return_value)
```

These must be called after eel.start(). This can be done by calling a Python function in JavaScript which calls this demonstrated method. Also I will explain soon about the non-blocking eel.start() which then means you could do this after the eel.start().

Calling a Python function with a return value from JavaScript is a bit harder due to the JavaScript language. Simply making a function async and using await will fix this though:

```javascript
async function run() {
  let return_value = await eel.py_random()(); // Must prefix call with 'await'
  console.log('Got this from Python: ' + return_value);
}

run();
```

This will allows us to wait for the value to be returned from the server. If you leave out await, you will be given a [Promise object](https://developers.google.com/web/fundamentals/primers/promises) which will only be given the actual value of return when the data is returned which will be a lot later due to the speed of transferring the data (fast for us but too slow for a computer).

## A Simple Example

In this example I will create to files, one being the Python script and the other being main.html in the web/ folder beside the Python script.

*server.py*
```python
import eel
import time

eel.init('web')

@eel.expose
def getTime():
    return time.strftime('%c')

eel.start('main.html')
```

*web/main.html*
```html
<html>
    <head>
        <title>My Page</title>
		<script type="text/javascript" src="/eel.js"></script>
        <script>
            async function getTime() {
                let value = await eel.getTime()();
                alert(value);
            }
        </script>
    </head>
    <body>
        <button onclick="getTime()">Click to get time</button>
    </body>
<html>
```

When running server.py, a chrome app window will appear with a button saying "Click to get time". When clicked, this will call the getTime() function in python and then return the value back to JavaScript on the line `let value = await eel.getTime()();`. I then alert this value.

![Get Time](/post-assets/python-gui-using-chrome/time.png)

## Do NOT use time.sleep()
`time.sleep()` is very dangerous when used with eel; fortunately we have been given an alternative. Calling `time.sleep()` will pause the execution of the whole server so you should use `eel.sleep()` instead. It has the exact same functionality, just it's one less import you need.

## Threading in Python
To reduce the chance of conflicts, eel also provides a interface for creating threads. Use `eel.spawn()` to replace threading instances. This is also helpful for creating thread in general.

An example of using `eel.sleep()` and `eel.spawn()`:

```python
import eel
eel.init('web')

def my_other_thread():
    while True:
        print("I'm a thread")
        eel.sleep(1.0)

eel.spawn(my_other_thread)
eel.start('main.html')
```

### Don't block eel.start()
If you want to execute code underneath eel.start() you can pass block=False as an argument to stop it from blocking. For example:

```python
eel.start('main.html', block=False)
```

This will allow code execution to keep flowing after it reaches this statement. Do note that when your code underneath eel.start() is complete the server will stop as the whole script has stopped.

## Why Use Eel?
So those who have used Flask, bottle or pyramid before may be asking why not just use those? When using a library like Flask, you need to create the server, setting up all the routes yourself and decide on the layout of the server.

With Eel, you don't need to do any of this; simply importing eel, calling `eel.init('web')` and `eel.start('main.html')` will create the whole server for you. Now all you need to do is create your methods and expose them to eel using a decorator.

## Common Issues and Questions

### Is it possible to package eel with pyinstaller?
Yes, if you look at Eel documentation, go [to the bottom](https://github.com/ChrisKnott/Eel#building-a-distributable-binary﻿) and it explains clearly how to do this.

## Extra Reading
 - [Eel GitHub Page](https://github.com/ChrisKnott/Eel)
 - [A demo of using Eel in a Python script](https://github.com/brentvollebregt/auto-py-to-exe/blob/master/run.py)
