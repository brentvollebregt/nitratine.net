---
templateKey: blog-post
title: "Encryption and Decryption in Python"
date: 2018-09-16T12:00:00.000Z
category: YouTube
tags: [python, encryption, cyber-security]
image: feature.png
description: "In this post, I discuss how to encrypt and decrypt messages in Python using symmetric encryption. I will demonstrate how to create keys, save keys and how to encrypt messages and text."
disableToc: false
hidden: false
youtubeVideoId: H8t4DJ3Tdrg
---

Using the [cryptography](https://cryptography.io/en/latest/) module in Python, we will use an implementation of AES called [Fernet](https://cryptography.io/en/latest/fernet/) to encrypt data. I will also show you how to keep keys safe and how to use these methods on files.

## Installing cryptography

Since Python does not come with anything that can encrypt files, we will need to use a third-party module.

[PyCrypto](https://github.com/dlitz/pycrypto) is quite popular but since it does not offer built wheels, if you don't have Microsoft Visual C++ Build Tools installed, you will be told to install it. Instead of installing extra tools just to build this, I will be using the cryptography module. To install this, execute:

```console
python -m pip install cryptography
```

To make sure it installed correctly, open IDLE and execute:

```python
import cryptography
```

If no errors appeared it has been installed correctly.

## What is Symmetric Encryption?

[Symmetric encryption](https://en.wikipedia.org/wiki/Symmetric-key_algorithm) is when a key is used to encrypt and decrypt a message, so whoever encrypted it can decrypt it. The only way to decrypt the message is to know what was used to encrypt it; kind of like a password.

To use symmetric encryption, we will use the [Fernet class](https://cryptography.io/en/latest/fernet/) which is an implementation of [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)

> Looking for a tutorial on asymmetric encryption? [I wrote one of those for Python too](/blog/post/asymmetric-encryption-and-decryption-in-python/).

## Getting a Key

There are two main ways to get a key, we can either generate a new one or use one that has previously been generated. These keys need to be in a particular format so make sure to get this right.

To generate a new random key, we can simply use

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
```

The variable _key_ will now have the value of a URL safe base64 encoded key. When using these keys to encrypt, make sure to keep them safe, if you lose them you will not be able to decrypt your message.

This key will have a type of bytes, so if you want a string you can call `key.decode()` to convert from UTF-8 to Pythons string type.

### Storing Keys

One way of keeping your keys safe is to keep them in a file. To do this we can simply create/overwrite a file and put the key in it.

```python
file = open('key.key', 'wb')
file.write(key) # The key is type bytes still
file.close()
```

> Make sure to keep these files safe and don't give them to anyone that you don't trust. Anyone with these keys can decrypt all past messages encrypted with this key.

### Reading Keys

If you have previously saved your key using the method I showed, you can read the key back out using the following code.

```python
file = open('key.key', 'rb')
key = file.read() # The key will be type bytes
file.close()
```

The key will now be read into the variable _key_ and will be type bytes.

### Generating a Key From A Password

If you want to base your key of a string that the user can input or some other form of input, you can create a key using this input.

```python
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password_provided = "password" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
```

The variable _key_ will now have the value of a url safe base64 encoded key.

> It is recommended to use a different salt than the one shown here. You can generate a new salt using os.urandom(16). Make sure to use the same salt every time you convert a password to a key otherwise it will not produce the same result.

## Encrypting

To encrypt a message, you will need a key (as previously discussed) and your message as type bytes (you can convert strings to bytes using `.encode()`).

```python
from cryptography.fernet import Fernet
message = "my deep dark secret".encode()

f = Fernet(key)
encrypted = f.encrypt(message)
```

The variable _encrypted_ will now have the value of the message encrypted as type bytes. This is also a URL safe base64 encoded key.

## Decrypting

To decrypt a message, you will need the same key and the encrypted message (still in bytes).

```python
from cryptography.fernet import Fernet
encrypted = b"...encrypted bytes..."

f = Fernet(key)
decrypted = f.decrypt(encrypted)
```

The variable _decrypted_ will now have the value of the original message (which was of type bytes).

## Demonstration

To show this in action, here is a properly constructed example.

```python
>>> from cryptography.fernet import Fernet
>>> message = "my deep dark secret".encode()
>>> key = Fernet.generate_key() # Store this key or get if you already have it
>>> f = Fernet(key)
>>> encrypted = f.encrypt(message)
>>> decrypted = f.decrypt(encrypted)
>>> message == decrypted
True
>>>
```

This example shows a key being generated, you will want to make sure you have already sorted your key out and put it in a file for later use.

## Encrypting and Decrypting Files

We can also encrypt files using this method since files can be read as bytes. Simply open the file, read the bytes, encrypt the data and write them out to a new file. To encrypt:

```python
from cryptography.fernet import Fernet
key = b'' # Use one of the methods to get a key (it must be the same when decrypting)
input_file = 'test.txt'
output_file = 'test.encrypted'

with open(input_file, 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)

with open(output_file, 'wb') as f:
    f.write(encrypted)

# You can delete input_file if you want
```

And then to decrypt a file:

```python
from cryptography.fernet import Fernet
key = b'' # Use one of the methods to get a key (it must be the same as used in encrypting)
input_file = 'test.encrypted'
output_file = 'test.txt'

with open(input_file, 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.decrypt(data)

with open(output_file, 'wb') as f:
    f.write(encrypted)

# You can delete input_file if you want
```

> As stated in [Fernet docs](https://cryptography.io/en/latest/fernet/#limitations), beware of large files; Fernet is ideal for encrypting data that easily fits in memory. You may need to think of methods to split larger files up to use this encryption method on large files.
