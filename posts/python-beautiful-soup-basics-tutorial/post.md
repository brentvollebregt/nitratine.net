title: "Python Beautiful Soup Basics Tutorial"
date: 2020-08-22
category: Tutorials
tags: [python, html, scraping]
feature: feature.png
description: "This tutorial covers the basics of the Python Beautiful Soup library including installation, parsing HTML/XML, finding elements and getting element data."

[TOC]

## What is Beautiful Soup?
Beautiful Soup is a Python library for pulling data out of HTML and XML files. It is commonly used for scraping websites and simply getting data out of a known HTML/XML structure.

There is awesome documentation for Beautiful Soup at [www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) which covers all of the functions that are to offer and many examples. In this tutorial, I will cover a subset of the functions provided with examples that I feel will give a good starting point to someone new. I will cover some common expectations of a library like Beautiful Soup including:

- Searching for elements
- Getting element contents and attributes
- Getting the children and parent of an element 

## Getting Your Data To Parse
Before you start using Beautiful Soup, you'll first need to get your data source ready. For most of my examples, I'll be using some hard-coded example HTML. Here are a few ways you could source your data.

### String literal
A string literal is simply a string with your HTML or XML in it; for example:

```python
html = """
<html>
    <head>
        <title>Page title</title>
    </head>
    <body>
        ... body ...
    </body>
</html>
"""
```

### HTML or XML File
If your HTML or XML is in a file, you will need to read it into a variable so Beautiful Soup can use it; for example:

```python
file_path = "my_file.html"

file = open(file_path, 'r')
html = file.read()  # The html variable now has the HTML document in it 
file.close()
```

The variable `html` will have your data now like the [String literal](#string-literal) example.

### HTTP Request
If you want to get a webpage, you can use something like the [`requests` library](https://requests.readthedocs.io/en/master/) to get the page. Say you want to get [https://example.com/](https://example.com/), you would do:

```python
import requests

response = requests.get('https://example.com/')
html = response.content.decode()  # The html variable now has the HTML document in it 
```

The variable `html` will have your data now like the [String literal](#string-literal) example.

## Installing Beautiful Soup
To install Beautiful Soup, simply go to the command line and execute:

`python -m pip install beautifulsoup4`

> If you can't import `BeautifulSoup` later on, make sure you're 100% sure that you installed Beautiful Soup in the same distribution of Python that you're trying to import it in. Go to my tutorial on [How to Manage Multiple Python Distributions](https://nitratine.net/blog/post/how-to-manage-multiple-python-distributions/) if you're having some issues or are unsure.
    
## Using Beautiful Soup


### Parsing Your HTML/XML
When you have your HTML or XML data, you now want Beautiful Soup to parse it into a `BeautifulSoup` object using the following:

```python
from bs4 import BeautifulSoup

html = "..."

soup = BeautifulSoup(html, 'html.parser')
```

The variable `soup` now contains a [BeautifulSoup object](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup) that you can use to traverse the root element.

> Note: In all of the following examples, the variable `html` contains the HTML defined above the usage of it.

### The Four Main Kinds Of Objects
When using Beautiful Soup, you will encounter four types of objects, these are:

> Please note different types of objects that could be returned, these are just common ones.

#### BeautifulSoup
The BeautifulSoup object represents the parsed document as a whole. It inherits the [Tag](#tag) object so most calls you can make on a Tag object, you can also make on a BeautifulSoup object.

```html
<html lang="en">
    <head></head>
    <body></body>
</html>
```

```pycon
>>> soup = BeautifulSoup(html, 'html.parser')
>>> type(soup)
<class 'bs4.BeautifulSoup'>
```

#### Tag
A `Tag` object corresponds to an XML or HTML tag in the original document.

```pycon
>>> soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
>>> tag = soup.find('b')  # Get the b tag
>>> type(tag)
<class 'bs4.element.Tag'>
```

The `Tag` object allows us to access attributes on a tag using dictionary-like methods and also search for other tags under this tag.

To get the name of the current tag, access `tag.name`:

```pycon
>>> soup = BeautifulSoup('<span>Example tag</span>', 'html.parser')
>>> tag = soup.span
>>> tag.name
'span'
```

This tutorial covers more of what we can get out of a Tag under [Getting Data From An Element / Tag And Other Elements](#getting-data-from-an-element-tag-and-other-elements).

#### NavigableString
A NavigableString corresponds to a bit of text within a tag. When accessing the content of a `Tag` object, a `NavigableString` object will be returned.

```pycon
>>> soup = BeautifulSoup('<span>Example tag</span>', 'html.parser')
>>> tag = soup.span
>>> tag.string
<class 'bs4.element.NavigableString'>
```

To make this a string and drop the object altogether, cast the object to a string: `str(tag.string)`.

### Ways to Search For Elements / Tags

#### Searching Using `.find` vs `.find_all`
On any `BeautifulSoup` or `Tag` object, we can search for elements under the current tag (`BeautifulSoup` will have the root tag majority of the time). To search for other elements/tags, we can use `.find` and `.find_all`.

These two calls are very similar, they both take the same inputs, but `.find` returns the first tag found whereas `.find_all` returns all tags found if there are any. 

For example, if we had the following `BeautifulSoup` object:

```html
<div>
    <span>Span1</span>
    <a>A1</a>
    <span>Span2</span>
    <p>P1</p>
    <p>P2</p>
    <span>Span3</span>
</div>
```

```python
soup = BeautifulSoup(html, 'html.parser')  # html contains above data
```

Using `.find` to get the first span, we would do:

```pycon
>>> span = soup.find('span')
>>> span
<span>Span1</span>
```

This returned object is of type `bs4.element.Tag` so we could further search under this tag. If there was no matching element, we would get `None`, for example:

```pycon
>>> form = soup.find('form')
>>> form is None  # Validate that form is None for this example
True
```

Using `.find_all` to get all the spans, we would do:

```pycon
>>> spans = soup.find_all('span')
>>> spans
[<span>Span1</span>, <span>Span2</span>, <span>Span3</span>]
```

This has returned a list of `bs4.element.Tag` objects, so pulling out an individual object would allow us to perform more tag operations. If there was no matching element, we would get an empty list, for example:

```pycon
>>> forms = soup.find_all('form')
>>> forms
[]
```

All of the following examples will use one of `.find` or `.find_all` but they can both be used interchangeably to get the first or all of the target elements.

#### Search For Elements By Tag Name
As displayed in the examples above, using `.find` or `.find_all` and passing a tag name, we can search for elements with a specific tag. For example, if we had:

```html
<div>
    <span>Span1</span>
    <a>A1</a>
    <p>P1</p>
</div>
```

```python
soup = BeautifulSoup(html, 'html.parser')  # html contains above data
```

If we wanted to get the `a` tag, we would execute:

```pycon
>>> soup.find('a')
<a>A1</a>
```

If we wanted to get the `p` tag, we would execute:

```pycon
>>> soup.find('p')
<p>P1</p>
```

#### Search For Elements By Id
Passing the `id` argument to `.find` allows us to search for an element by id, for example:

```html
<div>
    <span>Element 1</span>
    <p id="not_target">Element 2</p>
    <a id="target">Element 3</a>
    <div>Element 4</div>
</div>
```

```pycon
>>> soup = BeautifulSoup(html, 'html.parser')  # html contains above data
>>> element = soup.find(id='target')  # The id we're searching for is "target"
>>> element  # Output the contents of `element`
<a id="target">Element 3</a>
```

Notice how this has found the element with the id "target" regardless of its tag name. 

#### Search For Elements By Class Name
Similar to searching by an id, we can also search for elements with a specific class by passing the class we want to search for, for example:

```html
<div>
    <span class="class_a class_b">Element 1</span>
    <p class="class_b class_c class_d">Element 2</p>
    <a class="class_c">Element 3</a>
    <div>Element 4</div>
</div>
```

```pycon
>>> soup = BeautifulSoup(html, 'html.parser')  # html contains above data
>>> elements = soup.find_all(class_='class_c')  # The class we're searching for is "class_c"
>>> elements
[<p class="class_b class_c class_d">Element 2</p>, <a class="class_c">Element 3</a>]
```

In this example, we found both the element with just the class "class_c" and the element with "class_c" being within other classes. This shows that this search will find the class name anywhere in the class attribute.

Note that we had to use `class_` as an argument to `.find_all`; this is because `class` is a reserved keyword in Python.

#### Search For Elements By A Combination Of Attributes
Using the elements above, we can search for elements with multiple attributes. To do this, the first positional argument is always the tag name and the other keyword arguments are attribute names. For example, if we had something like:

```html
<div>
    <h2>Heading 1</h2>
    <p>Data 1</p>
    <h2 class="bold">Heading 2</h2>
    <p class="bold">Data 2</p>
    <h2>Heading 3</h2>
    <p>Data 3</p>
</div>
```

And wanted to identify the p element with the class "bold", we would do:

```pycon
>>> soup = BeautifulSoup(html, 'html.parser')  # html contains above data
>>> element = soup.find('p', class_='bold')  # Searching for p tag with class "bold"
>>> element
<p class="bold">Data 2</p>
```

We are not only bound to search for tags, id and classes though; as stated above, providing other keyword arguments allows us to search for other attributes. 

For example, if we have:

```html
<div>
    <iframe src="https://example.com/" title="Example"></iframe>
    <iframe src="http://nitratine.net/" title="Nitratine"></iframe>
</div>
```

We can get the iframe with the title "Nitratine" by doing:

```pycon
>>> soup = BeautifulSoup(html, 'html.parser')  # html contains above data
>>> element = soup.find(title='Nitratine')  # Searching for anything with a title equal to "Nitratine"
>>> element
<iframe src="http://nitratine.net/" title="Nitratine"></iframe>
```

#### Search For Elements By Text Content
Aside from searching for things on the element itself, we can search for an element using expected text content. For example, if we have:

```html
<div>
    <p class="class_a">This is a paragraph</p>
    <p class="class_b">This is also a paragraph</p>
</div>
```

And we want to get the element with the text "This is also a paragraph" to check what class it has, we can do:

```pycon
>>> soup = BeautifulSoup(html, 'html.parser')  # html contains above data
>>> element = soup.find('p', string='This is also a paragraph')  # `string` is the internal string
>>> element
<p class="class_b">This is also a paragraph</p>
```

In the example above, we said to search for a p tag with the text "This is also a paragraph". We needed to specify the tag name otherwise we would get back a NavigableString object as shown below.

```pycon
>>> string = soup.find(string='This is also a paragraph')
>>> type(string)
<class 'bs4.element.NavigableString'>
>>> string
'This is also a paragraph'
```

However, to get around providing the tag it's in, we can get the parent of the NavigableString object to get the p tag that it's located in.

```pycon
>>> string = soup.find(string='This is also a paragraph')
>>> element = string.parent  # Go up the tree to get the parent element / tag
>>> element
<p class="class_b">This is also a paragraph</p>
```

#### Search For Elements Using a Query Selector
For anyone that has used CSS or JavaScripts `document.querySelector` / `document.querySelectorAll`, Beautiful Soup offers methods to search by CSS selectors. Using `.select()` and `.select_one()`, we can pass a CSS selectors to get elements/tags. 

The difference between `.select()` and `.select_one()` is like `.find()` and `.find_all()`; `.select()` finds many like `.find_all()` and `.select_one()` finds only one like `.find()`.

Lets say we had:

```html
<div>
    <h1>Title</h1>
    <p>Content 1</p>
    <p class="red">Content 2</p>
    <p>Content 3</p>
</div>
```

```python
soup = BeautifulSoup(html, 'html.parser')  # html contains above data
```

And wanted to find the p tag with the class "red", we would do:

```pycon
>>> element = soup.select_one('p.red')  # Pass in CSS selector
>>> element
<p class="red">Content 2</p>
```

If we had used `soup.select()`, we would get a list with the single item:

```pycon
>>> elements = soup.select('p.red')
>>> elements
[<p class="red">Content 2</p>]
```

Using this same idea, we can also get all the p tags:

```pycon
>>> elements = soup.select('p')
>>> elements
[<p>Content 1</p>, <p class="red">Content 2</p>, <p>Content 3</p>]
```

#### Searching Using Lambdas
For searching that needs some more advanced logic, you can pass a lambda to the `.find()` / `.find_all()` functions to do a more powerful search. For example, if we had:

```html
<div>
    <div id="header">
        <h1>My Title</h1>
        <p>Some text...</p>
    </div>
    <div id="main_content">
        <p>Content 1</p>
        <p>Content 2</p>
        <p>Content 3</p>
        <blockquote>Not Content</blockquote>
    </div>
    <div id="footer">
        <span>A footer element</span>
        <span>Another footer element</span>
    </div>
</div>
```

```python
soup = BeautifulSoup(html, 'html.parser')  # html contains above data
```

And we wanted to get the all the p tags under the div with the id "main_content", we could do:

```pycon
>>> elements = soup.find_all(lambda tag: tag.name == 'p' and tag.parent.attrs.get('id', None) == 'main_content')
>>> elements
[<p>Content 1</p>, <p>Content 2</p>, <p>Content 3</p>]
```

We can see that **every** tag in the parsed tree has been passed to the lambda function which then checks if the tag is a p tag and that the id attribute on its parent is "main_content".

> We will look at what `Tag.name`, `Tag.parent` and `Tag.attrs` are soon.

Sometimes these lambda searches can be less preformat than doing intermediate searches, thus you could chain searches as demonstrated below to speed this operation up.
 
#### Chaining Searches
When using one of the find or select queries to get a Tag object, you can also then use this Tag object to search further. Chaining searches can lead to performance increases as you reduce the search space for each step. For example, if we had what we used above:

```html
<div>
    <div id="header">
        <h1>My Title</h1>
        <p>Some text...</p>
    </div>
    <div id="main_content">
        <p>Content 1</p>
        <p>Content 2</p>
        <p>Content 3</p>
        <blockquote>Not Content</blockquote>
    </div>
    <div id="footer">
        <span>A footer element</span>
        <span>Another footer element</span>
    </div>
</div>
```

```python
soup = BeautifulSoup(html, 'html.parser')  # html contains above data
```

And we wanted to get all the p tags under the div with the id "main_content", we would do:

```pycon
>>> main_content_element = soup.find(id='main_content')  # First find the div tag using the id
>>> main_content_element  # Prove we have the div tag and all contents
<div id="main_content">
<p>Content 1</p>
<p>Content 2</p>
<p>Content 3</p>
<blockquote>Not Content</blockquote>
</div>
>>> elements = main_content_element.find_all('p')  # Find all p tags in the div tag we found
>>> elements
[<p>Content 1</p>, <p>Content 2</p>, <p>Content 3</p>]
```

### Getting Data From An Element / Tag And Other Elements
Once you have a Tag object, getting data off it is pretty easy.

#### Getting The Tag Name Of The Current Tag
To get the name of the current tag, we can call `tag.name`:

```pycon
>>> element
<p>Some text...</p>
>>> element.name
'p'
```

#### Getting The Text Inside The Current Tag
To get the text inside the current tag, we can call `tag.text` or `tag.string`:

```pycon
>>> element
<p>Some text...</p>
>>> element.text
'Some text...'
```

#### Getting The Attributes Of The Current Tag
To get the attributes inside the current tag, we can access them using `tag.attrs`. This will return something that looks and functions like a dictionary.

```pycon
>>> element
<p class="class_a, class_b, class_c" id="some_id" title="My Title"></p>
>>> element.attrs
{'id': 'some_id', 'class': ['class_a,', 'class_b,', 'class_c'], 'title': 'My Title'}
```

Notice how `id` and `title` have a string value whereas `class` has a list of string as its value; this is demonstrating Beautiful Soup handling attributes with multiple values. 

If you want to get a particular attribute from an element, we can use `.get()` as it may not always be there:

```pycon
>>> element
<p class="class_a, class_b, class_c" id="some_id" title="My Title"></p>
>>> element.attrs.get('id', None)
'some_id'
```

In the case the attribute does not exist, the second parameter passed to `.get()` is returned:

```pycon
>>> element
<p class="class_a, class_b, class_c" id="some_id" title="My Title"></p>
>>> element.attrs.get('doesntexist', None)
None
```

#### Getting The Parent Of The Current Tag
To get a tags parent (the tag it's located in), we can call `tag.parent`:

```pycon
>>> element
<p>Some text...</p>
>>> element.parent
<div id="header">
<h1>My Title</h1>
<p>Some text...</p>
</div>
```

> None will be returned if the element has no parent

#### Getting The Children Of The Current Tag
To get all the elements under a given element, we can call `tag.children`:

```pycon
>>> element
<div id="header">
<h1>My Title</h1>
<p>Some text...</p>
</div>
>>> element.children
<list_iterator object at 0x000001E2E5BE25C8>
>>> list(element.children)
['\n', <h1>My Title</h1>, '\n', <p>Some text...</p>, '\n']
```

This has returned an iterator which finds the children on-demand to potentially reduce memory and CPU consumption. We can see that this has also returned elements that look like `'\n'`; looking at these more closely, we can see they are NavigableString objects:

```pycon
>>> list(element.children)[0]
'\n'
>>> type(list(element.children)[0])
<class 'bs4.element.NavigableString'>
```

## Examples

### Example 1 - Scraping Data From A Table
- Data source: Custom
- Target: Read the HTML table into a Python array

HTML preview:

```html
<html>
    <head>
        <title>Page Title</title>
    </head>
    <body>
        <h1>Title</h1>
        <p>Some contents...</p>
        <table>
            <tr>
                <th>Firstname</th>
                <th>Lastname</th>
                <th>Age</th>
            </tr>
            <tr>
                <td>Jill</td>
                <td>Smith</td>
                <td>50</td>
            </tr>
            <tr>
                <td>Eve</td>
                <td>Jackson</td>
                <td>94</td>
            </tr>
        </table>
    </body>
</html>
```

Getting the table data:

```python
from bs4 import BeautifulSoup

html = '<html from above>'

soup = BeautifulSoup(html, 'html.parser')
table_element = soup.find('table')  # Get the table element
row_elements = table_element.find_all('tr')  # Get all rows in the table

data_rows = []
for element in row_elements:  # Loop over each row
    cell_elements = element.find_all(lambda tag: tag.name in ['th', 'td'])  # Get all the cells in the row that are either th or td
    cell_values = [str(e.string) for e in cell_elements]  # Get the content out of each cell and cast the values to a string
    data_rows.append(cell_values)  # Add this row to our data
    
print(data_rows)  # Output the data that is now in data_rows
```

Output:

```python
[
    ['Firstname', 'Lastname', 'Age'],
    ['Jill', 'Smith', '50'],
    ['Eve', 'Jackson', '94']
]
```

### Example 2 - Read A Single Value On The Page
- Data source: testing-ground.scraping.pro/whoami *(No longer exists)*
- Target: Read IP address

HTML preview (cut down version):

```html
<html>
    <title>Web Scraper Testing Ground</title>
  </head>
  <body>
    <a href="/" style="text-decoration: none;">
      <div id="title">WEB SCRAPER TESTING GROUND</div>
      <div id="logo"></div>
    </a>
    <div id="content">
      <h1>WHO AM I?</h1>
      <div id="caseinfo">
        <p>
          This page displays web client information and can be used for web
          scraper tuning.
        </p>
        <p>
          It also sets <em>TestingGround=WebScraperTest</em> cookie that you can
          check whether your web scrapes keeps cookies or not.
        </p>
      </div>

      <div id="case_whoami">
        <div class="name">IP</div>
        <div class="value" id="IP">23.126.45.124</div>
        <div class="name">HOST</div>
        <div class="value" id="HOST">testing-ground.scraping.pro</div>
        <div class="name">REFERER</div>
        <div class="value" id="REFERER">
          http://testing-ground.scraping.pro/
        </div>
        <div class="name">USER AGENT</div>
        <div class="value" id="USER_AGENT">
          Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
          like Gecko) Chrome/84.0.4147.135 Safari/537.36
        </div>
        <div class="name">COOKIES</div>
        <div class="value" id="COOKIE"><ul></ul></div>
      </div>
    </div>
  </body>
</html>
```

Getting the IP address:

```python
from bs4 import BeautifulSoup

html = '<html from above>'

soup = BeautifulSoup(html, 'html.parser')
ip_element = soup.find(id="IP")  # Get the element with the id "IP"
ip = ip_element.text  # Get the text from the element

print(ip)  # Output the ip
```

Output:

```python
'23.126.45.124'
```
