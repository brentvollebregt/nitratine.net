title: "Python Encryption and Decryption with PyCryptodome"
date: 2019-05-14
category: Tutorials
tags: [python, encryption, cyber-security]
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

## What is AES?
In this tutorial, I'll be using the implementation of [Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) (AES) to encrypt strings and files. If you do not know what AES is, I highly recommend you understand what it is and how it works before you continue with the examples. Not understanding the different modes of AES and how it is designed could lead to insecure encryptions.

AES has a block size of 128 bits and this implementation of AES supports 3 sizes of keys, 16, 24 or 32 bytes long respectively for *AES-128*, *AES-192* or *AES-256*. Many modes are [supported by this implementation of AES](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html), including:

- CBC: Cipher-Block Chaining
- CFB: Cipher FeedBack
- OFB: Output FeedBack
- CTR: Counter
- EAX: EAX
        
> I have not included Electronic Code Book (ECB) due to the fact that [it is not semantically secure](https://crypto.stackexchange.com/a/20946). I do not recommend using this mode.
 

## Generating A Key
Keys that are used in AES must be 128, 192, or 256 bits in size (respectively for *AES-128*, *AES-192* or *AES-256*). PyCryptodome supplies a function at `Crypto.Random.get_random_bytes` that returns a random byte string of a length we decide. To use this, import the function and pass a length to the function:

```python
from Crypto.Random import get_random_bytes
key = get_random_bytes(32) # 32 bytes * 8 = 256 bits (1 byte = 8 bits)
print(key)
```

When running this snippet, a new key that is of type bytes will be generated on each run. When using this method for creating a key, it will need to be stored somewhere to be used again.

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

A [salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) is *random data that is used as an additional input to a one-way function that "hashes" data*. How you store this is up to you, in short terms, it is combined with the password provided by the user so that the result cannot be looked up in a [rainbow table](https://en.wikipedia.org/wiki/Rainbow_table). Even though not 100% recommended, I feel it can be more beneficial to simply generate a salt and hard-code it into your application. To generate a salt, we can use the same method that we used to generate a key:

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

> Even though it may be ok to hard code a salt for your own projects, it is recommended to generate a new salt for each object encrypted. When storing data (as you will see later), you can write the salt to the beginning of the file (assuming your storage method is a file) as it is a fixed length. When decrypting the file, read out the salt first, then generate the key with the password and then continue to read the rest of the data out of the file to decrypt.

## Encrypting
Now that we have the key, we can encrypt files. These methods encrypt bytes objects, so if you have a string, you can call `.encode()` on it, otherwise for other objects, make sure they are of type bytes. 

> In these examples, I will show a variable named `key` which will be where your key should be (as generated from the instructions above).

You can find examples in the documentation for [legacy ciphers](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html) and [modern ciphers](https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html); I will cover a couple of examples from the documentation to help you understand how to encrypt and save the data required for decryption. 

Different modes will require you to store different values for decryption like an iv, nonce or tag. If you want to use a mode that I do not cover here, simply find the example in the docs (from the links above for legacy and modern ciphers) and identify what values need to be stored.

### CBC Example
You can find this example [in the docs](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cbc-mode). CBC requires you to pad your data to make sure the final block is filled with some data; not all modes require this (as I show in the next example).

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

output_file = 'encrypted.bin' # Output file
data = b'Your data....' # Must be a bytes object
key = b'YOUR KEY' # The key you generated

# Create cipher object and encrypt the data
cipher = AES.new(key, AES.MODE_CBC) # Create a AES cipher object with the key using the mode CBC
ciphered_data = cipher.encrypt(pad(data, AES.block_size)) # Pad the input data and then encrypt

file_out = open(output_file, "wb") # Open file to write bytes
file_out.write(cipher.iv) # Write the iv to the output file (will be required for decryption)
file_out.write(ciphered_data) # Write the varying length ciphertext to the file (this is the encrypted data)
file_out.close()
```

### CFB Example
You can find this example [in the docs](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cfb-mode). CFB is very similar to CFB but does not require the data to be padded; this means the call `pad(data, AES.block_size)` from the CBC example can be replaced with `data` for CFB. 

This CFB mode example is practically identical to the OFB mode (just need to change the mode in `AES.new`) and very close to CTR in the way that a nonce needs to be stored compared to the iv from CFB (the nonce is stored in `cipher.nonce`).

> CFB, OFB and CTR to not require padding because they are stream ciphers, not block ciphers

```python
from Crypto.Cipher import AES

output_file = 'encrypted.bin'
data = b'Your data....'
key = b'YOUR KEY'

cipher = AES.new(key, AES.MODE_CFB) # CFB mode
ciphered_data = cipher.encrypt(data) # Only need to encrypt the data, no padding required for this mode

file_out = open(output_file, "wb")
file_out.write(cipher.iv)
file_out.write(ciphered_data)
file_out.close()
```

### EAX Example
You can find this example [in the docs](https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-aes). Just like all the examples here and in the docs for AES, the steps are all the same, just different data needs to be stored for this mode being a nonce, tag and the ciphered data.

```python
from Crypto.Cipher import AES

output_file = 'encrypted.bin'
data = b'Your data....'
key = b'YOUR KEY'

cipher = AES.new(key, AES.MODE_EAX) # EAX mode
ciphered_data, tag = cipher.encrypt_and_digest(data) # Encrypt and digest to get the ciphered data and tag

file_out = open(output_file, "wb")
file_out.write(cipher.nonce) # Write the nonce to the output file (will be required for decryption - fixed size)
file_out.write(tag) # Write the tag out after (will be required for decryption - fixed size)
file_out.write(ciphered_data)
file_out.close()
```

### How To Use All The Outputs From These Encryptions?
Many of these modes will output more than one value; this could be in the form of an iv, nonce or something else. To pack all this data in a file, put the data that has  static lengths (always the same) at the top of the file, then ciphered content after this. Now when you read out the file, you can read x amount of bytes using `.read(x)` to get the known-length values (can be multiple) and then call `.read(-1)` to get the rest of the data.

In the examples above, this is how I saved all the data required to a file, but you do not have to save the data this way. When only using the data internally or in something like a database, it can be easier to just keep them separate in their own variable or column.

Another way to do this would be to convert all the iv, nonce, tag and ciphered text output values to base64. You can now create a Python dictionary object using the names of these variables as keys and base64 values as the values and save this as a JSON file. This makes it very easy to write and read but will make larger files that take longer to read/write. For example:

```python
import json
from base64 import b64encode, b64decode

# These are placeholders for the values that we need to store to be read out later to decrypt. You may require other values than these like the tag or nonce
ciphertext = b'...'
iv = b'...'

# Create the Python dictionary with the required data
output_json = {
    'ciphertext': b64encode(ciphertext).decode('utf-8'),
    'iv': b64encode(iv).decode('utf-8')
}

# Save this dictionary to a JSON file
with open('encrypted_file.json', 'w') as outfile:
    json.dump(output_json, outfile)


# Now to get all the data for decryption:
with open('encrypted_file.json') as infile:
    input_json = json.load(infile)

# Get all the fields from the dictionary read from the JSON file
ciphertext = input_json['ciphertext']
iv = input_json['iv']
```
 
## Decrypting
Now that you have your data, stored it somewhere, you will want to read it and decrypt it. Based on the encryption examples above, these are the examples to decrypt. If you did not store the data in a file, you can populate the required fields using whatever method you used to store them.

### CBC Example
When the file for the CBC encryption example was written, the iv was first written and then the ciphered data. Since we know the length of the iv (16 bytes), first read that from the start of the file and the read the rest of the file to get the ciphered data.

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

input_file = 'encrypted.bin' # Input file
key = b'YOUR KEY' # The key used for encryption (do not store/read this from the file)

# Read the data from the file
file_in = open(input_file, 'rb') # Open the file to read bytes
iv = file_in.read(16) # Read the iv out - this is 16 bytes long
ciphered_data = file_in.read() # Read the rest of the data
file_in.close()

cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result
```

### CFB Example
In the CFB encryption example the iv and ciphered data was saved to the output file.

```python
from Crypto.Cipher import AES

input_file = 'encrypted.bin'
key = b'YOUR KEY'

file_in = open(input_file, 'rb')
iv = file_in.read(16)
ciphered_data = file_in.read()
file_in.close()

cipher = AES.new(key, AES.MODE_CFB, iv=iv)
original_data = cipher.decrypt(ciphered_data) # No need to un-pad
```

### EAX Example
In the EAX encryption example the nonce, tag and ciphered data was saved to the output file. We know the length of the nonce and tag values so we can read these out first and then the data after.

```python
from Crypto.Cipher import AES

input_file = 'encrypted.bin' # Input file (encrypted)
key = b'YOUR KEY' # The key you generated (same as what you encrypted with)

file_in = open(input_file, 'rb')
nonce = file_in.read(16) # Read the nonce out - this is 16 bytes long
tag = file_in.read(16) # Read the tag out - this is 16 bytes long
ciphered_data = file_in.read() # Read the rest of the data out
file_in.close()

# Decrypt and verify
cipher = AES.new(key, AES.MODE_EAX, nonce)
original_data = cipher.decrypt_and_verify(ciphered_data, tag) # Decrypt and verify with the tag
```

## Examples
In these examples, I will use the CFB mode to show that the input data can be encrypted and then decrypted to give the original input data. 

In each example I will generate a new key that will be used in the session; as described before, you will need to generate a key yourself and save it for encryption and decryption since encryption and decryption most likely won't be done in the same session (you can't rely on `get_random_bytes` to get your key back).

### String Example Proof
In this proof, I will demonstrate how to encrypt and decrypt a string.

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(32) # Use a stored / generated key
data_to_encrypt = 'This is plain text!' # This is your data

# === Encrypt ===

# First make your data a bytes object. To convert a string to a bytes object, we can call .encode() on it
data = data_to_encrypt.encode('utf-8')

# Create the cipher object and encrypt the data
cipher_encrypt = AES.new(key, AES.MODE_CFB)
ciphered_bytes = cipher_encrypt.encrypt(data)

# This is now our data
iv = cipher_encrypt.iv
ciphered_data = ciphered_bytes

# From here we now assume that we do not know data_to_encrypt or data (we will use it for proof afterwards
# We do know the iv, data and the key you have stored / generate

# === Decrypt ===

# Create the cipher object and decrypt the data
cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=iv)
deciphered_bytes = cipher_decrypt.decrypt(ciphered_data)

# Convert the bytes object back to the string
decrypted_data = deciphered_bytes.decode('utf-8')

# === Proving the data matches ===

# Now we prove that the original data is the same as the data we just ciphered out (running these should throw no errors)
assert data_to_encrypt == decrypted_data, 'Original data does not match the result'
```

### File Example Proof
In this proofm I will demonstrate how to encrypt and decrypt a file. This example will be a bit different from the examples above as I will be reading and writing to and from files using a buffer. This allows me to encrypt much larger files without the whole file having to be loaded into memory.

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(32) # Use a stored / generated key
file_to_encrypt = 'my_file.txt'
buffer_size = 65536 # 64kb

# === Encrypt ===

# Open the input and output files
input_file = open(file_to_encrypt, 'rb')
output_file = open(file_to_encrypt + '.encrypted', 'wb')

# Create the cipher object and encrypt the data
cipher_encrypt = AES.new(key, AES.MODE_CFB)

# Initially write the iv to the output file
output_file.write(cipher_encrypt.iv)

# Keep reading the file into the buffer, encrypting then writing to the new file
buffer = input_file.read(buffer_size)
while len(buffer) > 0:
    ciphered_bytes = cipher_encrypt.encrypt(buffer)
    output_file.write(ciphered_bytes)
    buffer = input_file.read(buffer_size)

# Close the input and output files
input_file.close()
output_file.close()

# === Decrypt ===

# Open the input and output files
input_file = open(file_to_encrypt + '.encrypted', 'rb')
output_file = open(file_to_encrypt + '.decrypted', 'wb')

# Read in the iv
iv = input_file.read(16)

# Create the cipher object and encrypt the data
cipher_encrypt = AES.new(key, AES.MODE_CFB, iv=iv)

# Keep reading the file into the buffer, decrypting then writing to the new file
buffer = input_file.read(buffer_size)
while len(buffer) > 0:
    decrypted_bytes = cipher_encrypt.decrypt(buffer)
    output_file.write(decrypted_bytes)
    buffer = input_file.read(buffer_size)
    
# Close the input and output files
input_file.close()
output_file.close()

# === Proving the data matches (hash the files and compare the hashes) ===
import hashlib

def get_file_hash(file_path):
    block_size = 65536
    file_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        fb = f.read(block_size)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(block_size)
    return file_hash.hexdigest()
    
assert get_file_hash(file_to_encrypt) == get_file_hash(file_to_encrypt + '.decrypted'), 'Files are not identical'
```

> If you look at the size of the .encrypted file, you would notice it is 16 bytes larger than the file that was encrypted. This is because the iv is at the start of the file for you to read back out.

> If are interested in hashing files in Python, check out my tutorial on [How to Hash Files in Python](/blog/post/how-to-hash-files-in-python/).
