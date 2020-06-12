---
templateKey: blog-post
title: "New Zealand Cyber Security Challenge 2019 Round 0 Solutions"
date: 2019-06-10T12:00:00.000Z
category: General
tags: [ctf, nzcsc]
image: feature.png
description: "These are my solutions to the challenges I solved in the New Zealand Cyber Security Challenge 2019 Round 0."
disableToc: false
hidden: false
---

## What is the [New Zealand Cyber Security Challenge](https://nzcsc.org.nz/)?
Each year the University of Waikato holds a "cybersecurity" competition which involves CTF for rounds 1 and 2, policy creation/identification for round 3 and attack/defend servers for the top 5 teams. Side Challenges are also held which varies with the theme per year.

> Unfortunately, I was not able to solve all challenges in round 0 this year so this solution guide will be incomplete unless extra contributions are provided. 

## Solutions

### Challenge 1
Presented with a login which is in HTML form. Looking at the DOM, the HTML forms `onsubmit` attribute is `login(event)`. Going to the console in Chrome DevTools and executing `login` shows a snippet of the function, click on this will then bring us to the source.

This function simply takes the username and password and posts it to `./login.php` using a `XMLHttpRequest`. The `onload` is defined which when the `responseText` is equal to `'yes'`, it will then go to `./done.php`

So this means we can skip the login completely and go to the page `./done.php`. An easy way to get this page is to create an anchor tag on the current page: `<a href="./done.php">done</a>`.

> `flag:4a78327703d7`

### Challenge 2
We are told that a simple XOR cipher is used to "protect our communications" and to check we have the correct key to validate against the examples, which are:

| Ciphertext in base64             | Plaintext                |
|----------------------------------|--------------------------|
| bVQwJ2M3K0pCIjQm                 | Test message             |
| ekghNjF6HVxSNiEqLjcZcisyLzYrV1Ym | Cyber Security Challenge |
| bVkmcyU2L14RKiBjMiddVSY9YzgrVV40 | The flag is hidden below |
| X10iNHk5fQ4HIGBxPnwPU3c=         | [REDACTED]               |

It was pretty easy to guess that the last row contained the flag and we could assume all the other rows used the same key. Since *[plaintext XOR key = cipher-text]* then *[cipher-text XOR plaintext = key]*; this means we only need one cipher-text and it's corresponding plain text to get the key. Using Python, I could get the key using this method:

```python
import base64

base64_ciphertext = 'bVkmcyU2L14RKiBjMiddVSY9YzgrVV40'
plaintext = 'The flag is hidden below'

def bxor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    
# Decode the cipher-text to a byte string and make the plaintext a byte string
key = bxor(base64.b64decode(base64_ciphertext), plaintext.encode())
```

The key produced from this was `91CSCZN91CSCZN91CSCZN91C`. We can see this repeats so we could say `91CSCZN` is the "base key" that repeats. Now to use this key on the final row, since `bxor` will zip to whatever byte string is the shortest, we do not have to make the key the correct size.

```python
import base64

base64_ciphertext = 'X10iNHk5fQ4HIGBxPnwPU3c='
key = '91CSCZN91CSCZN91CSCZN91C'

def bxor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

flag = bxor(base64.b64decode(base64_ciphertext), key.encode())
```

> This gives `flag:c376c32d26b4`

### Challenge 2*
In the DOM of challenge 2, there is another ciphertext hidden: `fnQXc211KwwAJ2B2PyoXUyo9`. Using the key on this:

```python
import base64

base64_ciphertext = 'fnQXc211KwwAJ2B2PyoXUyo9'
key = '91CSCZN91CSCZN91CSCZN91C'

def bxor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

text = bxor(base64.b64decode(base64_ciphertext), key.encode())
```

This gives text = `GET ./e51d35ed.bin`. Making an anchor tag on the page again to go to that relative URL as I did previously, the [file](https://nzcsc.org.nz/competition/2019/r0/2/challenge/e51d35ed.bin) is downloaded.

 This file is 50KB in size and was the end of the line for me unfortunately. No magic bytes match this file and [hexedit](https://hexed.it/) couldn't tell me the file type. I tried many things with this file but nothing gave a flag. I did notice though that there were no bytes in the file that had a value above 127; not sure if this hinted anything.

### Challenge 3
This challenge displayed an input that apparently allowed you to run commands, tying `help` gave `Available commands: file, ls, cat, head, tail`. Doing `ls` in the current directory, we could see `flag` (not the flag), `notflag` (not the flag), `index.php` and some folders/files.

Executing `cat index.php` gave the source PHP file of the current page, in here we could see inputs were being checked by a regex: `^(ls|file|cat|head|tail)( \-?(\.|\.{3})?\/?\w*| index\.php)?$`. Using this in [regex101](https://regex101.com/) I found that we could execute `ls ...`. After executing this, I saw there was a file named `flag` in the directory above.

Trying the regex out a bit more, I found we could execute `cat .../flag` which then printed the contents

> flag:8adb200631cc

### Challenge 4
Challenge 4 simply had the flag in the images EXIF data. I used [fotoforensics.com](http://fotoforensics.com/) to look at the exit data of the image.

> flag:85ad6ba312d9

### Challenge 4*
I searched quite a bit for this done but didn't get a lead on anything.

### Challenge 5
This challenge is a basic SQL injection. Searching the provided name `Fitzgerald Kemp` returned some information. Searching `' OR '1' = '1` gave all the data and a simply Ctrl+F on the page found the flag.

> flag:cc228b6984a9


### Challenge 6
This challenge supplies you a .ova file you can import to virtual box. When imported, a small Linux OS is presented with the file `validate` at /home/tc. When run, it asks you for a flag and waits a few seconds before saying if it's correct for not.

When I was first attempting this, I had written a shell script using vi on the VM (lord help me) to get all the strings out of `validate` and run them through the program. Obviously this didn't work because they learnt their lesson from last year.

I decided to extract the ova file using 7-Zip on a windows machine and then unzipped `VM-disk001.vmdk` within. Looking in \home\tc I could then easily access the `validate` file. I then went to [onlinedisassembler.com](https://onlinedisassembler.com/static/home/index.html) for a dirty way to look at what this binary contained.

Looking at the strings within the binary on a more familiar interface, I noticed hours later that one of the "flags" (many to put you off - which I had tested them all previously) were reversed; this was the flag.

> flag:51bd3c2fdb67


### Challenge 6*
Using the `validate` I had gotten from the .ova file, I opened up Kali Linux and put it in a proper disassembler. Running the program then stopped as it waited for input. I noticed a few commands above the breakpoint, that there had been a value constructed: `https://nzcsc.org.nz/competition/2019/r0/6/challenge/server.php?key=72a145aff16bb741310d7c953070807b`.

Requesting this using Python gave the flag:


```python
import requests
r = requests.get('https://nzcsc.org.nz/competition/2019/r0/6/challenge/server.php?key=72a145aff16bb741310d7c953070807b')
print(r.text)
```

> bonus:b55d54a59457
