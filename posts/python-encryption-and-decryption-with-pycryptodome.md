title: "Python Encryption and Decryption with PyCryptodome"
date: 2019-05-09
category: Tutorials
tags: [python, encryption]
feature: feature.png
description: "PyCryptodome is a fork of PyCrypto that brings enhancements on top of the now unmaintained PyCrypto library. This tutorial demonstrates using the library by encrypting strings and files using AES."

[TOC]

## What is PyCryptodome?
PyCryptodome is a self-contained Python package of low-level cryptographic primitives that supports Python 2.6 and 2.7, Python 3.4 and newer, and PyPy.

PyCryptodome is a fork of PyCrypto that has been enhanced to add more implementations and fixes to the original PyCrypto library. Where possible, most of the algorithms in this library are implemented in pure Python; only  pieces that are extremely critical to performance (e.g. block ciphers) are implemented as C extensions.

The PyCryptodome library offers implementations for things like:

 - AES
 - Stream ciphers like Salsa20
 - Cryptographic hashes like SHA-2
 - Message Authentication Codes like HMAC
 - RSA asymmetric key generation
 - [and much more!](https://www.pycryptodome.org/en/latest/src/features.html)

### What Happened To [PyCrypto](https://www.dlitz.net/software/pycrypto/)?
Even though unstated on any official site by the owner (which is unfortunate), PyCrypto is currently unmaintained. The last commit that was made to the official [GitHub repository](https://github.com/dlitz/pycrypto) was on [Jun 21, 2014](https://github.com/dlitz/pycrypto/commit/7acba5f3a6ff10f1424c309d0d34d2b713233019).

Since PyCrypto has been unmaintained for a few years, there have been a few security vulnerabilities found which are listed on [www.cvedetails.com](https://www.cvedetails.com/vulnerability-list/vendor_id-11993/product_id-22441/Dlitz-Pycrypto.html). This is quite a worry as PyCrypto examples are still prominent in Python security search results. Since there is no warnings in the project or on the repository, the best we can do is to tell people.

As PyCryptodome is a modified fork of PyCrypto, it can be used in some situations as a drop-in-replacement for PyCrypto; you can read more about that [in the docs](https://www.pycryptodome.org/en/latest/src/vs_pycrypto.html).

## Installing PyCryptodome
The easiest way to install this library is to use pip. Open up the terminal/cmd and execute:

```console
python -m pip install pycryptodome
```

To make sure it installed correctly, open IDLE and execute:

```python
import pycryptodome
```

If no errors appeared it has been installed correctly.

## What is AES?
In this tutorial I'll be using the implementation of [Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) (AES) to encrypt strings and files. If you do not know what AES is, I highly recommend you understand what it is and how it works before you continue with the examples. Not understanding the different modes of AES and how it is designed could lead to insecure encryptions.

- Block size 128 and key sizes of 128, 192, or 256 bits
    - It must be 16, 24 or 32 bytes long (respectively for *AES-128*, *AES-192* or *AES-256*).

- Mode used
    - Other modes we can use
    - Dont use this mode 
    - Most well known:
        - ECB: Electronic Code Book
        - CBC: Cipher-Block Chaining
        - CFB: Cipher FeedBack
        - OFB: Output FeedBack
        - CTR: CounTer Mode
        
> I have not included Electronic Code Book (ECB) due to the fact that [it is not semantically secure](https://crypto.stackexchange.com/a/20946). I do not recommend using this mode.
 

## Generating A Key
Keys that are used in AES must be 128, 192, or 256 bits in size (respectively for *AES-128*, *AES-192* or *AES-256*). PyCryptodome supplies a function at `Crypto.Random.get_random_bytes` that returns a random byte string of a length we decide. To use this, import the function and pass a length to the function:

```python
from Crypto.Random import get_random_bytes
key = get_random_bytes(32) # 32 bytes * 8 = 256 bits (1 byte = 8 bits)
print(key)
```

When running this snippet, a new key that is of type bytes will generated on each run. When using this method for creating a key, it will need to be stored somewhere to be used again.

> Remember, the key we will use to decrypt will have to be the same key we encrypted with. So don't lose the key otherwise you lose the file contents!

### Storing a Key
Key generation may seem useless as you need to store it, but that is definitely not the case. Since this function creates truly random data, we could simply generate a key and then write it to a file on a USB (or some other secure place). When we encrypt/decrypt files, we then read this file from the USB and get the key out. Here is an example of this:

```python
from Crypto.Random import get_random_bytes
key_location = "F:\\my_key.bin" # A safe place to store a key. Can be on a USB or even locally on the machine (not recommended unless it has been further encrypted)

# Generate the key
key = get_random_bytes(32)

# Save the key to a file
file_out = open(key_location, "wb") # wb = write bytes
file_out.write(key)
file_out.close()

# Later on ... (assume we no longer have the key)
file_in = open(key_location, "rb") # Read bytes
key_from_file = file_in.read() # This key should be the same
file_in.close()

# Since this is a demonstration, we can verify that the keys are the same (just for proof - you don't need to do this)
assert key == key_from_file, 'Keys do not match' # Will throw an AssertionError if they do not match
```

Even though generating keys like this is definitely one of the better options, some people would rather use passwords provided from users. This is quite understandable as it makes it easier for users to use the application

### Generating A Key From A "Password"
The idea here is to generate a byte sequence of appropriate length from a string provided from the user. To do this we can use `Crypto.Protocol.KDF.PBKDF2` ([API reference](https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html#Crypto.Protocol.KDF.PBKDF2)). PBKDF2 allows us to generate a key of any length by simply passing a password and salt.

> PBKDF2 is used because PBKDF1 can only generate keys up to 160 bits long.

A [salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) is "random data that is used as an additional input to a one-way function that "hashes" data". How you store this is up to you, in short terms, it is combined with the password provided by the user so that the result cannot be looked up in a [rainbow table](https://en.wikipedia.org/wiki/Rainbow_table). Even though not 100% recommended, I feel it can be more beneficial to simply generate a salt and hard-code it into your application. To generate a salt, we can use the same method that we used to generate a key:

```python
from Crypto.Random import get_random_bytes
print(get_random_bytes(32)) # Print the salt to be copied to your script
```

Using the output from this snippet, you can now create a variable in your script and assign it to the value that was output. For example:

```python
# ... imports
salt = b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
# ... rest of your code
```

Now that the hard part is over, we can generate keys using user input. Passing the string provided by the user (password) and the salt that you just hard-coded in your script as well as declaring the output length, we can get the key.

```python
from Crypto.Protocol.KDF import PBKDF2

salt = b'...' # Salt you generated
password = 'password123' # Password provided by the user, can use input() to get this

key = PBKDF2(password, salt, dkLen=32) # Your key that you can encrypt with
```

Now in `key`, you will have the key that you can use in encryption. You do not have to store this key now as you can see that this can be generated every time regarding the user provides the same password.

## Encrypting
Now that we have the key, we can encrypt files. These methods encrypt bytes objects, so if you have a string, you can call `.encode()` on it, otherwise for other objects, make sure they are of type bytes. 

> In these examples I will show a variable named `key` which will be where your key should be (as generated from the instructions above).

You can find examples in the documentation for [legacy ciphers](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html) and [modern ciphers](https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html); I will cover some examples

### CBC Example
You can find this example [in the docs](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cbc-mode).

- Requires padding

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
```

### CFB Example
You can find this example [in the docs](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cfb-mode). This example is very similar to OFB and CTR (and cbc but don't use that).

### EAX Example
You can find this example [in the docs](https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-aes). To encrypt your data using a key generated previously:

```python
from Crypto.Cipher import AES

output_file = 'encrypted.bin' # Output file
data = b'Your data....' # Must be a bytes object
key = b'YOUR KEY' # The key you generated

# Create cipher object and encrypt the data
cipher = AES.new(key, AES.MODE_EAX) # Create a AES cipher object with the key using the mode EAX
ciphertext, tag = cipher.encrypt_and_digest(data) # Encrypt

file_out = open(output_file, "wb") # Open file to write bytes
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ] # Write the none, tag and encrypted data
```

This will

> Of course you do not have to write the output to a file; this is just showing it is possible. You can use the output from `cipher.encrypt_and_digest(data)` however you like.

### How To Use All The Outputs From These Encryptions?
Many of these modes will output more than one value; this could be in the form of a iv, nonce or something else. To save all this data in a file, put the data that have static lengths (always the same) at the top of the file, then content at the end. Now when you read out the file, you can read x amount of bytes using `.read(x)` to get the known-length values (can be multiple) and then call `.read(-1)` to get the rest of the data.

In the examples above I have done this, but when only using the data internally or in something like a database, it can be easier to just keep them separate in their own variable or column.

## Decrypting
Now that you have your data, stored it somewhere, you will want to read it and decrypt it. Based off the encryption examples above, these are the examples to decrypt. If you did not store the data in a file, you can populate the require fields using whatever method you used to store them.

### CBC Example

### CFB Example

### EAX Example

## Examples

### String Example Proof

### File Example Proof
