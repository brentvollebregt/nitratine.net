---
layout: post
title: "Python SQLite3 Basics"
date: 2018-05-06
categories: Youtube
tags: Python SQL
description: "In this post I will go over some basics of SQLite3. SQLite3 allows us to access a database using SQL that doesn't require a separate server. This means the database is stored in a single file and we directly connect to the file rather than through some third-party applications server."
---

* content
{:toc}

In this post I will go over some basics of SQLite3. SQLite3 allows us to access a database using SQL that doesn't require a separate server. This means the database is stored in a single file and we directly connect to the file rather than through some third-party applications server.

{% include embedYouTube.html content="SQj17D1Q_6s" %}

<!-- more -->

> Please note this is not a SQL tutorial, I explain where to use SQL, not how.

## Setting Up A Connection
SQLite3 comes with any python distribution so you don't need to download anything extra; simply import sqlite3 and you are ready.

```python
import sqlite3
```

Now create a connection to the database file. Dos this using sqlite3.connect(); a connection object will be returned so make sure to keep it.

```python
connection = sqlite3.connect('example.db')
```

> If the .db file does not exist already, one will be created.

Now create a cursor object which will let us interact with the database. We can do this using .cursor() on our connection object.

```python
cursor = connection.cursor()
```

With these three simple lines, you now have a connection to your database file and a cursor to execute queries with.

## Executing Statements
To execute statements, we can use .execute() on our cursor object. For example:

```python
cursor.execute('CREATE TABLE url (id INTEGER PRIMARY KEY, url TEXT, count INTEGER);')
cursor.execute('INSERT INTO url(url, count) VALUES(?, ?)', (url, 0))
```

This above example will create the table I have instructed. You can use .execute() to execute all your SQL commands and queries like creating a table, adding rows, modifying entries and even selecting data (will be described soon).

### What are the Question Marks?
In the code above, I used two question marks in the values. These are placeholders for external data. When you are passing external data into your database that you can not guarantee is 100% safe (don't assume), it is best practice to pass them in with methods provided by the sqlite3 library.

.execute() can take two arguments, the query and a tuple of data to be put into the query. In my example above, the first item in the tuple would be put in place of the first question mark, this will also happen for the second item and second question mark.

We use this to stop SQL injections and error happening from dynamic data being added to queries.

> It is possible to just add your values by using .format or adding strings together using '+' but this method is much more safe.

### Why Didn't You Add An Id?
One feature of SQLite is that if you have a integer as a primary key in a table, it will auto increment based off the last entry if you do not assign. This means I don't have to worry about making different id's for each entry as the library will take care of it for me.

This means after each entry is put into the table, each is assigned a different id being 1, 2, 3, 4, ect...

### Committing
When creating tables, adding rows and modifying values, the table is in a temporary state. To actually save the changes you need to call .commit() to the connection object. In this example I would use:

```python
connection.commit()
```

Just like other databases, this will save the changes made. If something else is accessing the database file at the same time, it will not be able to see your changes until you have committed.

### Rolling Back
If you made changes to a database and want to undo them, regarding you haven't committed these changes yet, you can call .rollback() to the connection object. In this example I would use:

```python
connection.rollback()
```

### Available Datatypes
Unlike the bigger SQL databases, SQLite come with only 5 datatypes. Although this may seem like an issue, it isn't; you still can implement what you need with these.

- **NULL**: A NULL value.
- **INTEGER**: A signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
- **REAL**: A floating point value, stored as an 8-byte IEEE floating point number.
- **TEXT**: A text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).
- **BLOB**: A blob of data, stored exactly as it was input.

## Getting Returned Values
When getting data from your database, just like before, you will want to call .execute() on the cursor object. For example:

```python
cursor.execute('SELECT id FROM url WHERE url=?', (url, ))
```

In this example I am getting the id of a particular url in my url table. To get the result of my query there are two common possible methods. Depending on how many items your query returns will determine what method you use.

### Fetch One Row In Returned Object
After executing your query using cursor.execute() you can now call .fetchone() on cursor to get one row that has been returned. For example:

```python
url_id = cursor.fetchone()
```

This will return a sqlite3.Row object which can easily be casted to a tuple. You can now get items out of the row using indexes. Since I only selected one column from the table I will have one value in my tuple in url_id; so to get this out I can use `url_id[0]` to get the id of the url.

If you have selected more than one item, these items will be in a tuple-like object just like above so once again we can use indexes to get values out for example use `url_id[2]` to get the 3rd (2nd since we start from 0) object out.

### Fetch All Row In Returned Object
Like above, we can call .fetchall() on an executed query. This will return multiple rows like above in a list object. For example:

```python
cursor.execute('SELECT id, url FROM url')
ids_and_urls = cursor.fetchall()
```

Based off this example, we now have tuples of ids and urls in a list object. You could now either look at particular rows or do a for loop over them like this:

```python
for row in ids_and_urls:
    print ("ID: {}".format( row[0] ))
    print ("URL: {}".format( row[1] ))
```

### Closing a Cursor
When you are done modifying and getting data from a database, it is recommended to close your cursor. This is so that other programs that may be using the database can access the database as only one cursor is allowed at a time.

This is most certainly not something you have to do if only one script/thread accesses the database at a time, the Python garbage collector will remove the object if you don't when the script ends.

### Using Keys in Fetched Data
It may seem a bit stupid to only be able to use indexes to get data out of a row object; and you would be right.

First we need to set the connections `row_factory` to `sqlite3.Row`. This needs to be executed before you set your cursor.
```python
connection.row_factory = sqlite3.Row
```
Now when you set your cursor, you will be returned sqlite3.Row objects instead of tuples.

Using .keys() we can get the keys that are used in the row object returned. For example:

```python
cursor.execute('SELECT id, url FROM url WHERE url=?', (url, ))
particualr_id_and_url = cursor.fetchone()
print (particualr_id_and_url.keys())
```

This will return a list of the keys for items in the row object. These keys will the the names of the columns for the selected data (which you will already know as you set them). So to get a value out of the row object using it's column name we use:

```python
print ("ID: {}".format( particualr_id_and_url['id'] ))
```

## Viewing a Database Without Commands
A great way to check what is in your database is to go to a site like [SQLite Viewer](http://inloop.github.io/sqlite-viewer/) where you can view a sqlite file online. Simply drop the file in the site and you will be able to look at the contents locally in a very easy matter.

On this site you can also temporarily makes changes to the database which allows you to test commands before running them on data else-where.

## Why Don't I Just Use MySQL or SQL Server?
One massive benefit of this package is that you don't need to have any extra server running to execute your commands. Everything is done with a file you have access to and you don't need to install any extra software.

## Extra Reading
 - [sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)
