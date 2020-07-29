title: "Python Requests Tutorial"
date: 2019-04-04
category: Tutorials
tags: [python, requests]
feature: feature.png
description: "This is a basic Python requests tutorial to help you get started with sending HTTP requests in Python. This will cover all the basics that you will need and want to know when making HTTP requests in Python."

[TOC]

## Introduction
The [`requests`](https://github.com/requests/requests) Python package is an HTTP library created by [Kenneth Reitz](https://github.com/kennethreitz). It is a very well known package in the Python community for making HTTP requests easy to create and call. This tutorial will cover the basics that you will need to know and will want to know when making HTTP requests in Python.

Learning how to send HTTP requests allows you to query websites and API's for data or even a webpage so you can scrape data out with something like [Beatifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

## Installation
To install the requests module, first make sure you have pip setup. If not, follow my [tutorial on setting up pip](/blog/post/how-to-setup-pythons-pip/). After making sure pip is working, execute `pip install requests`. When this is successful, open Python IDLE and execute `import requests`; if no errors occur, the requests module has been installed successfully.

## Making a Simple Request
Just like your browser does, you can request a web page using Python. Get the URL of a website and use the following code to download the content of the page.

```python
import requests

r = requests.get('https://nitratine.net/blog/')
print (r.text)
```

When executing this, a lot of text should be printed. This is the content returned by the site requested, in the case of using the URL demonstrated above, the content will be HTML that renders my blog feed.

In this example, I have called `requests.get` passing my URL to be fetched. This function then returns a `requests.models.Response` object. Using the `.text` attribute, I can look at the data that was returned by the URL I called.

> When a browser calls a web page, it initially requests the URL being visited and then calls other URLs that are referenced in the HTML document to render the page with the CSS, JS, image and other files required.

## Attributes You Should Know About
The `Response` object that was returned in the example above contains many useful attributes. Here are some ones you should know about:
 
 - `.content`: The raw content of the request
 - `.text`: The text content of the request
 - `.status_code`: The status code of the response; e.g. 200 OK, 404 Not Found, 418 Short and Stout...
 - `.headers`: The headers of the response
 - `.cookies`: The cookies returned in the response. You can access cookie value like you would use a dict: `response.cookies['logged_in']`.
 
To get the value of these attributes, use them as I did in the previous code example.

### .json()
If a site returns a JSON response, you can call `.json()` on the `Response` object to convert the JSON object in the response to a Python dictionary.

```python
import requests

request = requests.get('https://jsonplaceholder.typicode.com/todos/1')
data = request.json()
print('Title: ' + data['title'])
```

This saves the effort on deserializing the .text value using the [ast module](https://docs.python.org/3/library/ast.html#ast.literal_eval). 

## Downloading an Image and Other Files
Just like downloading a web page, you can also download other files like images or videos. Simply find the URL of the image/other file *(make sure it is the URL of the file, not the URL of the page it's on)* and use it like before; but this time put the content into a file.

```python
import requests

file_destination = 'nitratine-logo.png'
url = "https://nitratine.net/assets/img/logo.png"
response = requests.get(url)
if response.status_code == 200:
    with open(file_destination, 'wb') as f: # Make sure to use wb are we are writing bytes
        f.write(response.content)
```

If you expect the file to be large (or just want to use a stream), you can use a stream to write to the output file as you receive the data. This means as the data comes in, it is written to the output file so the data does not have to sit in memory.

```python
import requests

file_destination = 'multi-clipboard.gif'
url = 'https://nitratine.net/posts/multi-clipboard/multi-clipboard.gif'
r = requests.get(url, stream=True)
if r.status_code == 200:
    with open(file_destination, 'wb') as f:
        for chunk in r:
            # print('Writing chunk') # Uncomment this to show that the file is being written chunk-by-chunk when parts of the data is received
            f.write(chunk) # Write each chunk received to a file
```

> These examples have been modified from [stackoverflow.com/a/13137873](https://stackoverflow.com/a/13137873)

## Different Methods
When making a request to a URL/URI, different 'methods' can be used. These tell the server what sort of action you want to perform. HTTP defines actions like GET, POST, PUT, DELETE and many others.

To use these different methods, simply replace the `.get` with `.post`/`.put`/`.delete` or whatever method you are using. For example, if I wanted to delete a record in a REST API, I could use:

```python
import requests

r = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
assert r.status_code == 200 # Check for HTTP 200 (OK)
```

## Parameters in URLs
Instead of constructing a URL to add parameters to it, the requests module offers a method to add them automatically for you. Simply create your key-value pairs in a Python dictionary and then pass this to the `params` argument in the request method. For example:

```python
import requests

parameters = { 'key1' : 'value1', 'key2' : 'value2' }
r = requests.get('https://httpbin.org/get', params=parameters)
print (r.text)
```

To show that the parameters were added to the url, we can verify it using a PreparedRequest.

```python
import requests

parameters = { 'key1' : 'value1', 'key2' : 'value2' }
req = requests.Request('GET','https://httpbin.org/get', params=parameters)
prepared = req.prepare() # Get a PreparedRequest object
print (prepared.url)
```

> The output of the above script is "https://httpbin.org/get?key1=value1&key2=value2" as expected.

## Sending Data in HTTP Body
When making calls to endpoints that require data in the body, we can use form-encoded, JSON or raw bodies.

### Form Encoded Body
In cases where you want to send some form-encoded data (like a HTML form would submit), we can pass key-value pairs as we used above to the `data` parameter. The dictionary of your data will be form-encoded when the request is made. For example:

```python
import requests

body_data = { 'key1' : 'value1', 'key2' : 'value2' }
r = requests.post('https://example.com/create-something', data=body_data)
```

### JSON Body
Today, JSON bodies are becoming more popular over form-encoded key-value pairs; this is due to how much more compact JSON is over XML (XML and JSON are typically used to carry larger payloads). Fortunately, JSON bodies are as easy to create in the request module as form-encoded are.

Instead of passing your dictionary to the `data` parameter, pass it to `json`. When the request is made, the `Content-Type` header will automatically be set to `application/json` to tell the server that this is a JSON request.

```python
import requests

body_data = { 'key1' : 'value1', 'key2' : 'value2' }
r = requests.post('https://example.com/create-something', json=body_data)
```

### Raw Body
In the cases where you want to specify exactly what is in the body manually, simply provide the string to the `body` parameter. For example:

```python
import requests

body_data = "This is my body"
r = requests.post('https://example.com/create-something', data=body_data)
```

## Custom headers
Previously I discussed that the `Content-Type` header will automatically be set to `application/json` when passing data to `json`. We can set headers manually is a very similar way to how we have been sending data. Once again, create the header key-value pairs in a Python dictionary and then pass them to the `headers` parameter.

```python
import requests

header_data = {
    'User-Agent' : 'Python requests',
    'X-My-Header-Key' : 'My header value'
}
r = requests.post('https://example.com/', headers=header_data)
```

## This is Only The Basics
Please know that these are only the basics of the requests library and there is a lot more to offer from this library; this tutorial however, should help you understand what you need to do to request and send data.

If you want to read up more on this library, Google is full of answers but the docs at [docs.python-requests.org](https://docs.python-requests.org/en/master/user/quickstart/) is great for reference material.

## I Don't Have s Server, How Can I Test These?
[hookbin.com](https://hookbin.com/) is an amazing place to test requests. Simply create a new endpoint on the site (big pink button) and copy the URL at the top of the rendered page. Now whenever you make a request to that URL, refresh the page and you will be able to see the content of the request you made.
