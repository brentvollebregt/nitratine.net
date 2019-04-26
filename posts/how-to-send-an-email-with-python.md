title: "How to Send an Email With Python"
date: 2018-01-23
category: YouTube
tags: [python, email]
feature: email-example-3.png
description: "This script sends an email using python. By logging into a gmail account with python you can send emails using this tutorial. This tutorial shows you how to send basic emails and emails with files attached."

[TOC]

{% with video_id="YPiHBtddefI" %}{% include 'blog-post-embedYouTube.html' %}{% endwith %}

## Why Bother?
These scripts are used to send emails from a gmail account (can be configured for other email servers). This will allow you to send emails when your script finishes executing, has come to an error or just needs to send some data to you.

This data could be anything, statistics of a website, crash reports or even files! This is particularly helpful for scripts running in the cloud or other places that take longer than 5 seconds to get access to. Getting reports sent straight to your email is convenient and can be helpful for storage. Python 3 is used in this tutorial.

## Before You Start
Before you start this, make sure you have your gmail username and password ready. The account you are going to use must not have 2-Step Verification enabled as we will no longer be able to log in.

Next go to [https://myaccount.google.com/lesssecureapps](https://myaccount.google.com/lesssecureapps) and login if you need to. In this page you will want to flick the Allow less secure apps switch to on. This allows us to use less secure sign-in technology to login to the email server; note that this will make you account more vulnerable.

![Allow less secure apps switch](/post-assets/how-to-send-an-email-with-python/alsa1.png)

> If you want/do have 2-Step Verification enabled, read up on how to [sign in using an app password](https://support.google.com/accounts/answer/185833). This allows you to generate a password specifically for this 'application' which allows this script to be compatible with a Google account using 2-Step Verification.

## Simple Email
To start off, we will use the [smtplib module](https://docs.python.org/3/library/smtplib.html) which comes with python, so no need to install it using [pip]({{ url_for('blog_post', path='how-to-setup-pythons-pip') }}).

```python
import smtplib

email = 'myaddress@gmail.com'
password = 'password'
send_to_email = 'sentoaddreess@gmail.com'
message = 'This is my message'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
server.sendmail(email, send_to_email , message)
server.quit()
```

By changing the initial variables at the top, the email will be sent. Make sure to change:
- 'email' to your email address
- 'password' to your email address password
- 'send_to_email' to the email address you want to send the message to (can be the same as 'email')
- 'message' to what the message is you want to send

![Simple Email Example](/post-assets/how-to-send-an-email-with-python/email-example-1.png)

The image above shows the email that I received. It is very basic and has no subject line, we will add that next.

## Better Layouts
We will now add a subject, sender and receiver using the [email module](https://docs.python.org/3/library/email.html). This module is also already in python so no need to use pip.

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = 'myaddress@gmail.com'
password = 'password'
send_to_email = 'sentoaddreess@gmail.com'
subject = 'This is the subject'
message = 'This is my message'

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()
```

Replacing the previous variables again and setting the new variable 'subject' to the subject line, the email will now send with a subject line when run.

![Better Email Example](/post-assets/how-to-send-an-email-with-python/email-example-2.png)

The image above shows the email that I received. It now has a subject and has a to header if you click the little down arrow by 'me'.

## Attachments
There are quite a few ways to attach files to an email, but this is one of the simpler ways. This time we will use an encoder and MIMEMultipart from the email module and os.path to simply get the filename from the provided path.

This method supports text files, images, videos, audio and pdfs.

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

email = 'myaddress@gmail.com'
password = 'password'
send_to_email = 'sentoaddreess@gmail.com'
subject = 'This is the subject'
message = 'This is my message'
file_location = 'C:\\Users\\You\\Desktop\\attach.txt'

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(message, 'plain'))

filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()
```

Once again, replacing the previous variables but setting the new variable 'file_location' to the location of the tile that you want to send, the email will now send with the file attached.

![Attachment Email Example](/post-assets/how-to-send-an-email-with-python/email-example-3.png)

The image above shows the email that I received. It now has a file named 'test.py' that I declared in the script attached to the email.

## HTML in Emails
If you want to add thinks like links or css formatting to the email, you will need to prepare HTML text for the email.
Make another string which is the plain-text version of the html and then attach them both to the MIMEMultipart object to be sent later on.

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = 'myaddress@gmail.com'
password = 'password'
send_to_email = 'sentoaddreess@gmail.com'
subject = 'This is the subject'
messageHTML = '<p>Visit <a href="https://nitratine.net/">nitratine.net<a> for some great <span style="color: #496dd0">tutorials and projects!</span><p>'
messagePlain = 'Visit nitratine.net for some great tutorials and projects!'

msg = MIMEMultipart('alternative')
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(messagePlain, 'plain'))
msg.attach(MIMEText(messageHTML, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()
```

As needed before, change the variables at the top but also messageHTML and messagePlain this time, the email will now be displayed using the HTML provided.

![Attachment Email Example](/post-assets/how-to-send-an-email-with-python/email-example-4.png)

The image above shows that I received the email with the link and inline CSS colouring on the specified text.

## Sources
- [WikiBooks](https://en.wikibooks.org/wiki/Python_Programming/Email)
- [naelshiab.com](http://naelshiab.com/tutorial-send-email-python/)

*Most recently modified on 15-7-18 ( added video )*

