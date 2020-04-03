title: "XOR Python Byte Strings"
date: 2019-06-08
category: Snippets
tags: [python]
feature: feature.png
description: "This snippet shows you how to can simply XOR two Python byte strings using a function to produce another byte string."

[TOC]

Previously doing a CTF challenge I found myself needing to XOR two byte strings in Python to reveal a key from the original text and 'ciphered' data (in this case by XOR).

## String XOR

I found [an answer on stackoverflow](https://stackoverflow.com/a/2612730/) showing how to XOR two strings to form a resulting string:

```python
def sxor(s1,s2):    
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
```

Using this we could now do:

```python
key = sxor('string 1', 'string 2')
```

## Byte XOR

But this only worked for strings and I had a byte string. To fix this I simply removed the `ord` and `chr` calls to only manipulate bytes.

```python
def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
```

So now I could do

```python
key = byte_xor(b'string 1', b'string 2')
```