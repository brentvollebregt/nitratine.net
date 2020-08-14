title: "Python GCM Encryption Tutorial"
date: 2020-08-13
category: Tutorials
tags: [python, encryption, cyber-security]
feature: decryption-flow-diagram.png
description: "This tutorial covers what AES GCM mode encryption is, the benefits of it and how to use it in the PyCryptodome Python library to encrypt and decrypt files and other objects."

[TOC]

> This tutorial is a follow on from [Python Encryption and Decryption with PyCryptodome](/blog/post/python-encryption-and-decryption-with-pycryptodome/) which covers a high-level view of the usage of the Python PyCryptodome library. If you have already read this, there will be a bit of duplicate reading but I recommend at least skimming just in case you miss something.

## What is AES and GCM Mode?
[Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) (AES) is a fast, secure and very popular block cipher that is commonly used to encrypt electronic data. AES has three different block ciphers: _AES-128_ (128 bit), _AES-192_ (192 bit) and _AES-256_ (256 bit) - each cipher is named after the key length they use for encryption and decryption. Each of these ciphers encrypt and decrypt the data in 128-bit blocks but they use different sizes of cryptographic keys.

AES supports many different "modes". Modes are the internal algorithm used to encrypt data; each mode can potentially have different inputs and outputs but they always have a single input for data to encrypt and a single output for encrypted data along with an input key.

[_GCM_](https://en.wikipedia.org/wiki/Galois/Counter_Mode) is a mode of AES that uses the [CTR (counter) mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR)) to encrypt data and uses Galois mode for authentication. Aside from the CTR mode which is used to encrypt the data, Galois mode authentication allows us to check at the end of decryption that the message has not been tampered with. GCM is well known for its speed and that it's a mode that it's patent-free.

In this tutorial, I'll be using an implementation of AES in [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/) to encrypt strings and files. Many modes are supported [by this implementation of AES](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html), including CBC, CFB and GCM which we will be using. I chose PyCryptodome as it is well documented and is similar to an older package _PyCrypto_ that died a while ago.

## What is [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/)
PyCryptodome is a self-contained Python package of low-level cryptographic primitives that supports Python 2.6 and 2.7, Python 3.4 and newer, and PyPy.

PyCryptodome is a fork of PyCrypto that has been enhanced to add more implementations and fixes to the original PyCrypto library. Where possible, most of the algorithms in this library are implemented in pure Python; only pieces that are extremely critical to performance (e.g. block ciphers) are implemented as C extensions.

The library offers implementations for things like:

 - AES
 - Stream ciphers like Salsa20
 - Cryptographic hashes like SHA-2
 - Message Authentication Codes like HMAC
 - RSA asymmetric key generation
 - [and much more!](https://www.pycryptodome.org/en/latest/src/features.html)
 
### Why You Should Use PyCryptodome Over the Original PyCrypto
Even though unstated on any official site by the owner (which is unfortunate), PyCrypto is currently unmaintained. The last commit that was made to the official [GitHub repository](https://github.com/dlitz/pycrypto) was on [Jun 21, 2014](https://github.com/dlitz/pycrypto/commit/7acba5f3a6ff10f1424c309d0d34d2b713233019).

Since PyCrypto has been unmaintained for a few years, there have been a few security vulnerabilities found which are listed on [www.cvedetails.com](https://www.cvedetails.com/vulnerability-list/vendor_id-11993/product_id-22441/Dlitz-Pycrypto.html). This is quite a worry as PyCrypto examples are still prominent in Python security search results. Since there are no warnings in the project or on the repository, the best we can do is to tell people.

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

## Generating A Key
Keys that are used in AES must be 128, 192, or 256 bits in size (for *AES-128*, *AES-192* or *AES-256* respectively). In my post [Python Encryption and Decryption with PyCryptodome](/blog/post/python-encryption-and-decryption-with-pycryptodome/), I describe how to

- [How to generate a random key with PyCryptodome](/blog/post/python-encryption-and-decryption-with-pycryptodome/#generating-a-key)
- [How to store and read the randomly generated key](/blog/post/python-encryption-and-decryption-with-pycryptodome/#storing-a-key)
- [How to generate a key from a password](/blog/post/python-encryption-and-decryption-with-pycryptodome/#generating-a-key-from-a-password)
 
For this tutorial, I'll just go over how to generate a key from a password as it is the most popular method. You are still free to use a randomly generated key as demonstrated in the links above - they will still work with these examples.
 
When generating a key from a password, we need to take a string provided by the user and create an appropriately sized byte sequence; the method used must produce the same output for the same inputs. To do this we can use `Crypto.Protocol.KDF.scrypt` ([API reference](https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html#scrypt)). _scrypt_ allows us to generate a key of any length by simply passing a password and _salt_. 

> scrypt has been used instead of PBKDF2 because, in addition to being computationally expensive, it is also memory intensive and therefore more secure against the risk of custom ASICs.

scrypt is different from the SHA family (ie. _SHA-256_ and _SHA-512_) because it also takes a salt and a work factor. Providing a salt that will mean that the same hash does not map to the same password every time, thus preventing [rainbow table](https://en.wikipedia.org/wiki/Rainbow_table) lookups. A work factor is also specified to make the transformation more computationally difficult which means the key is harder to brute force.

> You can read more about the differences between password hashes differ and secure hashes in [this reply on Stack Exchange](https://crypto.stackexchange.com/a/35279) - in this example, PBKDF2 is compared to SHA-512 rather than scrypt.

### Generating a Salt

A [salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) is *random data that is used as an additional input to a one-way function that "hashes" data*. To generate a salt, we can use the function `Crypto.Random.get_random_bytes` provided by PyCryptodome:

```python
from Crypto.Random import get_random_bytes
salt = get_random_bytes(32)
```

If you execute `print(salt)` you will see something like the following

```python
b'\x8a\xfe\x1f\xa7aY}\xa3It=\xc3\xccT\xc8\x94\xc11%w]A\xb7\x87G\xd8\xba\x9e\xf8\xec&\xf0'
```

This is a random sequence of bytes that has been generated. For every object (like files) you will encrypt, you should generate a new salt for it to be combined with the password by scrypt. This will mean the same password does not create the same key for multiple objects.

It's safe to store this generated salt with the encrypted output and in this tutorial, I'll show you how to store them with the output and then read them back out. 

### Generating the Key Using scrypt
Now that you have generated a salt, we can generate a key using the password being provided. Passing the password provided by the user, the salt that you just generated as well as declaring the output length, we can get the key.

```python
from Crypto.Protocol.KDF import scrypt

salt = b'...'  # Salt you generated
password = 'password123'  # Password provided by the user, can use input() to get this

key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)  # Your key that you can encrypt with
```

Now in `key`, you will have the key that you can use in encryption - you can view it using `print(key)`. You do not have to store this key now as you can see that this can be generated every time regarding the user provides the same password as long as you use the same salt (which we will be storing with the encrypted file/object).

In the example above, `key_len` has been set to 32; this is the length of the key that we want to be output. 32 has been used because 32 * 8 bits (8 bits = 1 byte) is 256, this means we will be using AES-256 when providing the key generated by this function.

I also passed values for `N`, `r` and `p` which can be found in the [docs for scrypt](https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html#scrypt). `N` is the work factor (CPU/Memory cost) which will determine how long it takes to calculate the output - 2^14 will be <100ms whereas 2^20 will be <5s on today's machines. 

> I have left `N` as `2**17` to keep people happy about the timing of encryption - in the case of blind copy and paste. If you're implementing this in a critical system or want to add have scrypt return a slightly more secure derivation, I recommend bumping `N` to `2**20`.

## Source and Storage Planning
Before we begin, we need to do a bit of planning of what is being encrypted (the source) and any transformations required, the inputs and outputs for both encryption and decryption and storing values we need to remember with the encrypted file.

### Identifying Your Source and Transformations
In this example below, I will show you how to encrypt a file. If you are not using a file though, it may still be able to be encrypted.

If your object is in the form of bytes (`type(your_bytes_object) == bytes`) then you will have something like this:

```python
your_bytes_object = b'\xadd\x8d-\xef\xd5I\xe2u\x19\xb6\x00\xc0+\xad...'
```

To make this readable, we can convert it to a `BytesIO` object using the following

```python
import io
file_object = io.BytesIO(your_bytes_object)
```

Now `file_object` will look like a file because we can perform file-like operations on it like when we use `open` and call `.read()`.

If you have a string (`type(your_bytes_object) == str`), call `.encode()` on it to convert it to bytes and then follow the step above. Note that when the data is decrypted, you will need to call `.decode()` on the output bytes to turn it back into a string.

```python
import io

my_string_to_encrypt = 'Wow! This is a cool string.'
file = io.BytesIO(my_string_to_encrypt.encode())
```

### Encryption Planning
Here is a fully-involved diagram on the process we will need to follow to encrypt:

![Encryption Flow Diagram](/posts/python-gcm-encryption-tutorial/encryption-flow-diagram.png)

1. Generate a new salt.
2. Use `scrypt` to convert the salt and password into a key we can use.
3. Open a new file and write the salt out.
    - We write the salt to the output file first as we will need it when decrypting later.
    - Putting it in this file allows us to keep the correct salt with the encrypted data.
    - Putting it at the top of the file means we can easily read it out before decrypting (we know the length as it's always the same).
4. Create a new AES encryption instance using the key.
5. Write the nonce out to the file.
    - The nonce is a random byte sequence generated by the instances of AES and is the start of the counter in CTR mode.
    - This is different so if the same key and file and encrypted together again, the encryption will be different.
    - Just like the salt, this is also stored at the top of the file so we can read it out again before decrypting to tell the CTR mode where to start counting from.
6. Read some data from the file into a buffer and then give it to the encryption instance.
7. Write the encrypted data to the file.
    - 6 and 7 are repeated over and over again until there is no more data coming from the source file.
    - We read small parts out of the file at a time so we don't have to load the whole file into memory.
8. Write the tag to the output file.
    - This is the authentication "code" produced from the Galois mode authentication.
    - This is used in the decryption phase to identify tampering/corruption.


### Decryption Planning
Here is a fully-involved diagram on the process we will need to follow to decrypt:

![Decryption Flow Diagram](/posts/python-gcm-encryption-tutorial/decryption-flow-diagram.png)

1. Read the salt from the source file.
    - The salt we generated was 32 bytes long, so calling `.read(32)` will get the salt out of the encrypted file.
2. Use `scrypt` to convert the salt and password into a key again.
3. Read the nonce from the source file like we did for the salt.
    - AES GCM always generates a nonce that is 16 bytes long, so calling `.read(16)` will get the nonce out of the encrypted file.
4. Create a new AES decryption instance using the key and the nonce.
5. Read the encrypted file bit-by-bit and decrypt, then output each part to the output file. Leave the tag still in the file (16 bytes also) 
    - Just like when we read the file slowly to encrypt
6. Finally, read the tag and verify the decryption.


## Encryption

```python
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once


password = "password"  # Get this from somewhere else like input()

input_filename = 'input.txt'  # Any file extension will work
output_filename = input_filename + '.encrypted'  # You can name this anything, I'm just putting .encrypted on the end

# Open files
file_in = open(input_filename, 'rb')  # rb = read bytes. Required to read non-text files
file_out = open(output_filename, 'wb')  # wb = write bytes. Required to write the encrypted data

salt = get_random_bytes(32)  # Generate salt
key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)  # Generate a key using the password and salt
file_out.write(salt)  # Write the salt to the top of the output file

cipher = AES.new(key, AES.MODE_GCM)  # Create a cipher object to encrypt data
file_out.write(cipher.nonce)  # Write out the nonce to the output file under the salt

# Read, encrypt and write the data
data = file_in.read(BUFFER_SIZE)  # Read in some of the file
while len(data) != 0:  # Check if we need to encrypt anymore data
    encrypted_data = cipher.encrypt(data)  # Encrypt the data we read
    file_out.write(encrypted_data)  # Write the encrypted data to the output file
    data = file_in.read(BUFFER_SIZE)  # Read some more of the file to see if there is any more left
    
# Get and write the tag for decryption verification
tag = cipher.digest()  # Signal to the cipher that we are done and get the tag
file_out.write(tag)

# Close both files
file_in.close()
file_out.close()
```

The file `output_filename` will now have the encrypted data in it.


## Decrypting

```python
import os

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once


password = "password"  # Get this from somewhere else like input()

input_filename = 'input.txt.encrypted'  # The encrypted file
output_filename = 'decrypted.txt'  # The decrypted file

# Open files
file_in = open(input_filename, 'rb')
file_out = open(output_filename, 'wb')

# Read salt and generate key
salt = file_in.read(32)  # The salt we generated was 32 bits long
key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)  # Generate a key using the password and salt again

# Read nonce and create cipher
nonce = file_in.read(16)  # The nonce is 16 bytes long
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

# Identify how many bytes of encrypted there is
# We know that the salt (32) + the nonce (16) + the data (?) + the tag (16) is in the file
# So some basic algebra can tell us how much data we need to read to decrypt
file_in_size = os.path.getsize(input_filename)
encrypted_data_size = file_in_size - 32 - 16 - 16  # Total - salt - nonce - tag = encrypted data

# Read, decrypt and write the data
for _ in range(int(encrypted_data_size / BUFFER_SIZE)):  # Identify how many loops of full buffer reads we need to do
    data = file_in.read(BUFFER_SIZE)  # Read in some data from the encrypted file
    decrypted_data = cipher.decrypt(data)  # Decrypt the data
    file_out.write(decrypted_data)  # Write the decrypted data to the output file
data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))  # Read whatever we have calculated to be left of encrypted data
decrypted_data = cipher.decrypt(data)  # Decrypt the data
file_out.write(decrypted_data)  # Write the decrypted data to the output file

# Verify encrypted file was not tampered with
tag = file_in.read(16)
try:
    cipher.verify(tag)
except ValueError as e:
    # If we get a ValueError, there was an error when decrypting so delete the file we created
    file_in.close()
    file_out.close()
    os.remove(output_filename)
    raise e

# If everything was ok, close the files
file_in.close()
file_out.close()
```

The file `output_filename` will now have the original data in it.
