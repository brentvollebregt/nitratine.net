title: "How To Serve A React App From A Python Server"
date: 2020-08-29
category: Tutorials
tags: [python, react, flask]
feature: feature.png
description: "In this tutorial, I explain how to serve a React application from a Python Flask server and how we can set up a postbuild script to automatically move the build React app to the server after a build."

[TOC]

## Goal
The goal of this tutorial is to set up a directory with a React client and Python server where the Python server has the capability of serving a built React application.

> The server from this tutorial will serve a **built** React application, any changes made to the React app source will require it to be rebuild to be served by the server. You can still use `npm start` to locally develop the app.

This tutorial is for people that create frontends in React and would like to serve it from Python because their API is already in React or they just want to serve it from Python because they can. I will be going over the basics of getting the two set up in a way to work together.

## Setting Up The Folder Structure
When developing a client and server, you typically want to keep them in separate directories. To accomplish this, we will create two folders like below:

```text
📁 project-root
┣ 📁 client
┗ 📁 server
```

## Setting Up Your React Application
After setting up these folders, we need to put a React app into the "client" folder. If you want to use a pre-existing app, you will need to move it but if you don't we can create one now.

### Pre-existing React App
If you have a pre-existing React app you want to serve from the Python server, copy package.json and everything beside it into the "client" folder. You should have something that now looks like this:

```text
📁 project-root
┣ 📁 client
┃ ┣ 📁 node_modules
┃ ┣ 📁 public
┃ ┣ 📁 src
┃ ┣ 📜 .gitignore
┃ ┣ 📜 package.json
┃ ┣ 📜 package-lock.json
┃ ┣ 📜 README.md
┃ ┗ 📜 tsconfig.json
┗ 📁 server
```

You may have different files in the "client" folder which is ok - the only requirement is that your package.json, public, src and any other files required to run the application have been moved here.

You can also copy over the node_modules folder if you want. If you don't have a node_modules folder, execute `npm install` in the "client" directory to download all your required packages.

### Create A New React App
If you want to start with a new React app, cd into the "client" folder and then execute:

```terminal
npx create-react-app .
```

> You can alternatively create a TypeScript React app using `npx create-react-app . --template typescript`

After this completes, you should have something that looks like this:

```text
📁 project-root
┣ 📁 client
┃ ┣ 📁 node_modules
┃ ┣ 📁 public
┃ ┣ 📁 src
┃ ┣ 📜 .gitignore
┃ ┣ 📜 package.json
┃ ┣ 📜 package-lock.json
┃ ┗ 📜 README.md
┗ 📁 server
```

## Setting Up A Python Server
Now that the React app is in the right place, we can set up the Python app and get it serving a basic page to being with.

### Creating The Server
In the "server" folder, create a new file run.py:

```text
📁 project-root
┣ 📁 client
┃ ┗ ... react files
┗ 📁 server
  ┗ 📜 run.py
```

This file will be what runs the server.
 
> If you have a pre-existing server/API, you can also perform similar steps to set up the serving of the React app, although the setup may be different for your server. If you do want to use your current server, I recommended moving your current server into the "server" folder and skip making run.py as you can modify the file where all your other endpoints are.

To save on a lot of unnecessary code, we'll use [Flask](https://flask.palletsprojects.com/en/1.1.x/) to help set up the web-server. To start, install Flask by executing the following in a terminal:

```terminal
python -m pip install flask
```

After flask has been installed, we will then set the server up in run.py. Open run.py in IDLE or another editor of your choice and add the following:

```python
from flask import Flask  # Import flask

app = Flask(__name__)  # Setup the flask app by creating an instance of Flask

@app.route('/')  # When someone goes to / on the server, execute the following function
def home():
    return 'Hello, World!'  # Return this message back to the browser
    
if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    app.run()  # Start the server
```

> This snippet has been modified from [Flask's Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/) page.

Now run the server using IDLE or a terminal:

```terminal
python run.py
```

You should see a message like the following appear:

```text
$ python run.py
 * Serving Flask app "run" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

This means the server is now running and if you go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) you should see the text "Hello, World!" - this means the server is working and we can continue on to serving a page.

> Tip: Press [[Ctrl]] + [[C]] in the console running the server to stop it.

### Serving An HTML Page
Typically when serving an HTML page from a Flask server, you would put the HTML file in a "templates" folder beside the Flask app. In this tutorial however, we will soon be using the index.html file from the React build, so we can just serve it as a static file.

To prepare for this, create a file in "server/static" called index.html with a basic message:

```html
<html>
    <head>
        <title>An Example Page</title>
    </head>
    <body>
        <h1>An Example Page</h1>
    </body>
</html>
```

Here would be the new layout:

```text
📁 project-root
┣ 📁 client
┃ ┗ ... react files
┗ 📁 server
  ┣ 📁 static
  ┃ ┗ 📜 index.html     <-- new file
  ┗ 📜 run.py
```

After creating this new index.html file, we need to go back into run.py and make the server respond with this HTML file when someone requests a file from "/". We will change the `home` definition to return the file like this:  

```python
@app.route('/')
def home():  # At the same home function as before
    return app.send_static_file('index.html')  # Return index.html from the static folder
```

If you run the server again (like you did before) and go back to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) after the messages appear, you should see that the HTML in index.html was returned.

This is great! Now when someone requests for "/", index.html will be returned. You can press [[Ctrl]] + [[C]] again to stop the server for the moment.

## Moving React Build To The Server
We now want to set up a script that will copy the output of the React app build to the servers "static" folder so index.html can be served to the client.

### Postbuild Script
To do this, we will use an npm postbuild script (written in JavaScript) to copy all the output from `npm build` that had been put into the "build" folder to the server's "static" folder. The reason we will use a JavaScript script is because:

- It will be platform-independent (`rm`/`cp` terminal commands are not available in Windows cmd but are in Linux)
- We can run it with `node` which we can be sure will be available
- `node` will happily run JavaScript without having to be transpiled (like TypeScript)

Here is the script we will use to copy the build to the server:

```javascript
var path = require('path');
const fs = require("fs");

const targetSource = './build'; // Relative path to copy files from
const targetDestination = '../server/static'; // Relative path to copy files to

/**
 * Remove directory recursively
 * @param {string} dir_path
 * @see https://stackoverflow.com/a/42505874
 */
function rimraf(dir_path) {
    if (fs.existsSync(dir_path)) {
        fs.readdirSync(dir_path).forEach(function(entry) {
            var entry_path = path.join(dir_path, entry);
            if (fs.lstatSync(entry_path).isDirectory()) {
                rimraf(entry_path);
            } else {
                fs.unlinkSync(entry_path);
            }
        });
        fs.rmdirSync(dir_path);
    }
}

/**
 * Copy a file
 * @param {string} source
 * @param {string} target
 * @see https://stackoverflow.com/a/26038979
 */
function copyFileSync(source, target) {
    var targetFile = target;
    // If target is a directory a new file with the same name will be created
    if (fs.existsSync(target)) {
        if (fs.lstatSync(target).isDirectory()) {
            targetFile = path.join(target, path.basename(source));
        }
    }
    fs.writeFileSync(targetFile, fs.readFileSync(source));
}

/**
 * Copy a folder recursively
 * @param {string} source
 * @param {string} target
 * @see https://stackoverflow.com/a/26038979
 */
function copyFolderRecursiveSync(source, target, root = false) {
    var files = [];
    // Check if folder needs to be created or integrated
    var targetFolder = root ? target : path.join(target, path.basename(source));
    if (!fs.existsSync(targetFolder)) {
        fs.mkdirSync(targetFolder);
    }
    // Copy
    if (fs.lstatSync(source).isDirectory()) {
        files = fs.readdirSync(source);
        files.forEach(function (file) {
            var curSource = path.join(source, file);
            if (fs.lstatSync(curSource).isDirectory()) {
                copyFolderRecursiveSync(curSource, targetFolder);
            } else {
                copyFileSync(curSource, targetFolder);
            }
        });
    }
}

// Calculate absolute paths using the relative paths we defined at the top
const sourceFolder = path.resolve(targetSource);
const destinationFolder = path.resolve(targetDestination);

// Remove destination folder if it exists to clear it
if (fs.existsSync(destinationFolder)) {
    rimraf(destinationFolder)
}

// Copy the build over
copyFolderRecursiveSync(sourceFolder, destinationFolder, true)
```

This script needs to be placed beside package.json:

```text
📁 project-root
┣ 📁 client
┃ ┣ 📁 node_modules
┃ ┣ 📁 public
┃ ┣ 📁 src
┃ ┣ 📜 .gitignore
┃ ┣ 📜 package.json
┃ ┣ 📜 package-lock.json
┃ ┣ 📜 postbuild.js       <-- right here
┃ ┗ 📜 README.md
┗ 📁 server
  ┗ 📜 ... server files
```

We now want to setup package.json to run this script after an npm build. Create a new `"postbuild"` script key and set it's value value to `"node postbuild.js"`. Here is an example excerpt based off the default package.json generated before: 

```json
"scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
	"postbuild": "node postbuild.js",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
},
```

Now when you execute `npm build` in the "client" folder, all the files put in "build" will be copied to "server/static". To visualise the structure, we are going from:

```text
📁 project-root
┣ 📁 client
┃ ┣ 📁 build            <-- build files
┃ ┃ ┣ 📜 favicon.ico
┃ ┃ ┣ 📜 index.html
┃ ┃ ┣ 📜 manifest.json
┃ ┃ ┗ 📜 .. and other build files
┃ ┣ 📁 node_modules
┃ ┣ 📁 public
┃ ┣ 📁 src
┃ ┣ 📜 .gitignore
┃ ┣ 📜 package.json
┃ ┣ 📜 package-lock.json
┃ ┣ 📜 postbuild.js
┃ ┗ 📜 README.md
┗ 📁 server
  ┣ 📁 static
  ┗ 📜 run.py
```

to

```text
📁 project-root
┣ 📁 client
┃ ┣ 📁 build
┃ ┃ ┣ 📜 favicon.ico
┃ ┃ ┣ 📜 index.html
┃ ┃ ┣ 📜 manifest.json
┃ ┃ ┗ 📜 .. and other build files
┃ ┣ 📁 node_modules
┃ ┣ 📁 public
┃ ┣ 📁 src
┃ ┣ 📜 .gitignore
┃ ┣ 📜 package.json
┃ ┣ 📜 package-lock.json
┃ ┣ 📜 postbuild.js
┃ ┗ 📜 README.md
┗ 📁 server
  ┣ 📁 static            <-- build files copied to here
  ┃ ┣ 📜 favicon.ico
  ┃ ┣ 📜 index.html
  ┃ ┣ 📜 manifest.json
  ┃ ┗ 📜 .. and other build files
  ┗ 📜 run.py
```

> Don't worry the original index.html file being deleted as we'll now be using the one from the npm build that is associated with the React app.

## Running The Server After A Build
After you have run an `npm build` in the client folder and the build files have been copied to the server's static folder, we can now run the server again. After running the server and going to "/", you will notice that the index.html file has been served, but the console (when looking at devtools) shows many 404 requests.

These 404 requests have occurred because we are directly serving index.html but the other required React app files are at an unexpected path. Looking at devtools for example, a request has been made for `http://127.0.0.1:5000/manifest.json` which returned a 404, however if you go to `http://127.0.0.1:5000/static/manifest.json` you will see the file is under the "static/" path.

### The Last Piece Of The Puzzle
To get around this and make it a lot simpler for the client to request files, we can remove this "static/" part from the URL that the server is serving the static files from by changing [static_url_path](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.static_url_path). 

The `static_url_path` property is a value that can be supplied on the Flask instance initialisation which corresponds with the *URL prefix that the static route will be accessible from*. Since we can see that this is currently "static/" (from looking at the manifest.json file before), we can change it to be nothing by setting `static_url_path=''`.

To do this, update the Flask instance initialisation to:

```python
app = Flask(__name__, static_url_path='')
```

Now if you restart the server and go to "/", you will see the React app fully loads and there are no 404s.

This has been possible because Flask is matching any unknown routes with files in the static folder. Since we don't define routes for files like "manifest.json", these static files are returned.

## Usage And Workflow
### Development
Develop your React app using `npm start` in the "client" folder and execute `npm build` whenever you want to put your current changes in the server. You can run `npm build` as many times as you want to update the app that the server serves.

To run the Python server, execute `python run.py` in the "server" folder. The server will run forever but will need to be restarted it a new React app build is done.

### Development Using An API In The Python Server
If your Python server is the  React app, you can develop your React app using `npm start` and have your application point at the Python server that is being run with `python run.py`. You do not have to use the application served from the Python server to use the API.

To identify what URL to request, I quite often use something like:

```javascript
const api_root = process.env.REACT_APP_API_ROOT ? process.env.REACT_APP_API_ROOT : window.location.origin;
```

This allows me to set the environment variable `REACT_APP_API_ROOT` to state the location of the Python server for development. When building the application, do not set `REACT_APP_API_ROOT` so then the application being served from the Python server will use `window.location.origin`.

> An example of a value to set `REACT_APP_API_ROOT` to is `http://127.0.0.1:5000` as that is where the Python server is.

### Deploying / Release
When deploying this server, you will need to run `npm install` and `npm build` in the "client" directory before running the server. 

When committing to source control, you do not need to commit the React app build files that have been copied (or the original build folder for that matter). You can make sure you have the following in a .gitignore at the root of the project (beside the "client" and "server" folders).

```text
server/static
client/build
client/node_modules
```

## Final Code
Aside from the default create-react-app or your current React app, here are the final files from this tutorial:

**client/postbuild.js**

```javascript
var path = require('path');
const fs = require("fs");

const targetSource = './build'; // Relative path to move files from
const targetDestination = '../server/static'; // Relative path to move files to

/**
 * Remove directory recursively
 * @param {string} dir_path
 * @see https://stackoverflow.com/a/42505874
 */
function rimraf(dir_path) {
    if (fs.existsSync(dir_path)) {
        fs.readdirSync(dir_path).forEach(function(entry) {
            var entry_path = path.join(dir_path, entry);
            if (fs.lstatSync(entry_path).isDirectory()) {
                rimraf(entry_path);
            } else {
                fs.unlinkSync(entry_path);
            }
        });
        fs.rmdirSync(dir_path);
    }
}

/**
 * Copy a file
 * @param {string} source
 * @param {string} target
 * @see https://stackoverflow.com/a/26038979
 */
function copyFileSync(source, target) {
    var targetFile = target;
    // If target is a directory a new file with the same name will be created
    if (fs.existsSync(target)) {
        if (fs.lstatSync(target).isDirectory()) {
            targetFile = path.join(target, path.basename(source));
        }
    }
    fs.writeFileSync(targetFile, fs.readFileSync(source));
}

/**
 * Copy a folder recursively
 * @param {string} source
 * @param {string} target
 * @see https://stackoverflow.com/a/26038979
 */
function copyFolderRecursiveSync(source, target, root = false) {
    var files = [];
    // Check if folder needs to be created or integrated
    var targetFolder = root ? target : path.join(target, path.basename(source));
    if (!fs.existsSync(targetFolder)) {
        fs.mkdirSync(targetFolder);
    }
    // Copy
    if (fs.lstatSync(source).isDirectory()) {
        files = fs.readdirSync(source);
        files.forEach(function (file) {
            var curSource = path.join(source, file);
            if (fs.lstatSync(curSource).isDirectory()) {
                copyFolderRecursiveSync(curSource, targetFolder);
            } else {
                copyFileSync(curSource, targetFolder);
            }
        });
    }
}

// Calculate absolute paths using the relative paths we defined at the top
const sourceFolder = path.resolve(targetSource);
const destinationFolder = path.resolve(targetDestination);

// Remove destination folder if it exists to clear it
if (fs.existsSync(destinationFolder)) {
    rimraf(destinationFolder)
}

// Copy the build over
copyFolderRecursiveSync(sourceFolder, destinationFolder, true)
```

**client/package.json**

```json
{
  "name": "client",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^4.2.4",
    "@testing-library/react": "^9.5.0",
    "@testing-library/user-event": "^7.2.1",
    "react": "^16.13.1",
    "react-dom": "^16.13.1",
    "react-scripts": "3.4.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
	"postbuild": "node postbuild.js",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": "react-app"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}

```

> This is modified from the default create-react-app package.json. The only addition is `"postbuild": "node postbuild.js",`

**server/run.py**

```python
from flask import Flask  # Import flask

app = Flask(__name__, static_url_path='')  # Setup the Flask app by creating an instance of Flask

@app.route('/')  # When someone goes to / on the server, execute the following function
def home():
    return app.send_static_file('index.html')  # Return index.html from the static folder
    
# You can add your other routes here if you want
# You could event have other API routes that the React app requests

if __name__ == '__main__':  # If the script that was run is this script (we have not been imported)
    app.run()  # Start the server
```

