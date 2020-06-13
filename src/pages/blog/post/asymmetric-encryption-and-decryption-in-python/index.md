---
templateKey: blog-post
title: "Asymmetric Encryption and Decryption in Python"
date: 2018-09-16T12:00:00.000Z
category: Tutorials
tags: [python, encryption, cyber-security]
image: feature.png
description: "In this post, I demonstrate the usage of the cryptography module in Python by using using the asymmetric key method RSA to encrypt and decrypt messages."
disableToc: false
hidden: false
---

Using the [cryptography](https://cryptography.io/en/latest/) module in Python, this post will look into methods of generating keys, storing keys and using the asymmetric encryption method [RSA](<https://en.wikipedia.org/wiki/RSA_(cryptosystem)>) to encrypt and decrypt messages and files. We will be using [cryptography.hazmat.primitives.asymmetric.rsa](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/) to generate keys.

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

## What is Asymmetric Encryption?

If you read my article on [Encryption and Decryption in Python](/blog/post/encryption-and-decryption-in-python/), you will see that I only used one key to encrypt and decrypt.

[Asymmetric encryption](https://en.wikipedia.org/wiki/Public-key_cryptography) uses two keys - a private key and a public key. Public keys are given out for anyone to use, you make them public information. Anyone can encrypt data with your public key and then only those with the private key can decrypt the message. This also works the other way around but it is a convention to keep your private key secret.

## Getting a Key

To generate the two keys, we can call rsa.generate_private_key with some general parameters. The public key will be found in the object that holds the creation of the private key.

```python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
```

### Storing Keys

To store the keys in a file, they first need to be serialized and then written to a file. To store the private key, we need to use the following.

```python
from cryptography.hazmat.primitives import serialization
private_key = ... # Placeholder - you generated this before

pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open('private_key.pem', 'wb') as f:
    f.write(pem)
```

> You can password protect the contents of this file using [this top key serialization example](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#key-serialization).

To store the public key, we need to use a slightly modified version.

```python
from cryptography.hazmat.primitives import serialization
public_key = ... # Placeholder - you generated this before

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('public_key.pem', 'wb') as f:
    f.write(pem)
```

> Remember that public and private keys are different so you will have to use these methods for each key.

### Reading Keys

To get the keys out of the files, we need to read each file and then load them. To read the private key, use the following.

```python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )
```

> If you store the key with a password, set _password_ to what you used.

The variable _private_key_ will now have the private key. To read the public key, we need to use a slightly modified version.

```python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )
```

The variable _public_key_ will now have the public key.

## Encrypting

Due to how asymmetric encryption algorithms like RSA work, encrypting with either one is fine, you just will need to use the other to decrypt. Applying a bit of logic to this can create some useful scenarios like [signing](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#signing) and [verification](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#verification). For this example, I will assume that you keep both keys safe and don't release them since this example is only for local encryption (can be applied to wider though when keys are exchanged).

This means you can use either key but I will demonstrate using the public key to encrypt, this will mean anyone with the private key can decrypt the message.

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

message = b'encrypt me!'
public_key = ... # Use one of the methods above to get your public key

encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
```

## Decrypting

Assuming that the public key was used to encrypt, we can use the private key to decrypt.

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

encrypted = ... # From before (could have been stored then read back here)
private_key = ... # Use one of the methods above to get your public key (matches the public_key)

original_message = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
```

## Demonstration

To show this in action, here is a properly constructed example.

```python
# Generating a key
>>> from cryptography.hazmat.backends import default_backend
>>> from cryptography.hazmat.primitives.asymmetric import rsa
>>> private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
>>> public_key = private_key.public_key()

# Storing the keys
>>> from cryptography.hazmat.primitives import serialization
>>> pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
>>> with open('private_key.pem', 'wb') as f:
    f.write(pem)
>>>
>>> pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
>>> with open('public_key.pem', 'wb') as f:
    f.write(pem)

# Reading the keys back in (for demonstration purposes)
>>> from cryptography.hazmat.backends import default_backend
>>> from cryptography.hazmat.primitives import serialization
>>> with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
>>> with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

# Encrypting and decrypting
>>> from cryptography.hazmat.primitives import hashes
>>> from cryptography.hazmat.primitives.asymmetric import padding
>>>
>>> message = b'encrypt me!'
>>> encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
>>> original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Checking the results
>>> original_message
b'encrypt me!'
>>> message == original_message
True
```

## Encrypting and Decrypting Files

To encrypt and decrypt files, you will need to use read and write binary when opening files. You can simply substitute the values I previously used for `message` with the contents of a file. For example:

```python
f = open('test.txt', 'rb')
message = f.read()
f.close()
```

Using the variable _message_ you can then encrypt it. To store, you can use the general Python method when encryption returns bytes.

```python
encrypted = 'data from encryption'
f = open('test.encrypted', 'wb')
f.write(encrypted)
f.close()
```

Now to decrypt you can easily read the data from test.encrypted like the first bit of code in this section, decrypt it and then write it back out to test.txt using the second bit of code in this section.
