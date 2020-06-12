---
templateKey: blog-post
title: "How To Hash Passwords In Python"
date: 2019-05-20T12:00:00.000Z
category: Tutorials
tags: [python, hashing, cyber-security]
image: feature.png
description: "In this tutorial, I cover the usage of PBKDF2_HMAC to encrypt passwords with a salt using Python."
disableToc: false
hidden: false
---

## Why You Need To Hash Passwords
Whenever verifying a user or something similar with a password, you must **never** store the password in [plaintext](https://en.wikipedia.org/wiki/Plaintext). If an attacker finds a database of plaintext passwords, they can easily be used in combination with matching emails to login to the associated site/account and even used to attempt to log into other accounts since a lot of people use the same password.

A common method used today is to hash passwords when a password is provided. It is recommended to use a salt when hashing and store the salt with the hashed password. 

## Why Not Use [SHA-256](https://en.wikipedia.org/wiki/SHA-2) or Something Similar?
Secure Hash Algorithms are [one-way functions](https://en.wikipedia.org/wiki/One-way_function), that is, once plaintext is hashed, we cannot get the plaintext from the hash. This is good because it keeps the password hidden and allows for simple verification by hashing a password provided by the user and comparing it to the stored hash of the actual password.

Unfortunately, hashing algorithms like SHA-256 are very quick to compute, meaning many combinations of strings can be calculated at a high speed to try and match a particular hash. If an attacker  has gotten hold of password hashes that were hashed with something like SHA-256, they could try to generate every password possible and hash these to find a match for the password hashes; this is called brute-forcing. 

While today this is not very practical due to the search space for most passwords, a smaller subset approach can be taken called a dictionary attack. In plain terms, this is where a file/database is previously constructed containing possible passwords that are better guesses than generating every possible password. Another tactic to matching hashes is using [rainbow tables](https://en.wikipedia.org/wiki/Rainbow_table), which takes a more grouped approach on randomly generating passwords.

## Hashing Passwords With `pbkdf2_hmac`
One deference to these matching methods is to use a slower hashing method. Using a slower hashing method will mean that it takes longer to compute many hashes in a specific period, thus making it unrealistic to find matches in our lifetime.

[PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) is a key derivation function where the user can set the computational cost; this aims to slow down the calculation of the key to making it more impractical to brute force. In usage terms, it takes a password, salt and a number of iterations to produce a certain key length which can also be compared to a hash as it is also a one-way function.

With iterations set to a large number, the algorithm takes longer to calculate the result. This is completely fine for someone that only needs to make one or a couple of attempts at checking if a password is correct, however trying billions will take a very long time.

> Please note that using this method does not stop brute force / dictionary attacks or the use of rainbow tables, it simply makes these methods more computationally difficult.

[PBKDF2_HMAC](https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac) is an implementation of the PBKDF2 key derivation function using [HMAC](https://en.wikipedia.org/wiki/HMAC) as pseudorandom function. `pbkdf2_hmac` can be found in the `hashlib` library (which comes with Python) and is in Python 3.4 and above. `pbkdf2_hmac` takes five parameters:

 - `hash_name`: hash digest algorithm for HMAC
 - `password`: the password being turned into the key
 - `salt`: a randomly generated salt
 - `iterations`: iterations in the calculation (higher means more computation required)
 - `dklen`: length of the output key (not required)

### Generating a Salt
Before generating the key using `pbkdf2_hmac`, you need to generate a random salt. Salts make the search space larger in the case of brute-forcing and adds difficulty for rainbow tables; using a salt only requires you to do a little more work and store an extra random byte sequence.

Salts do not need to be hidden, encrypted or hashed; this is because they are simply combined with the password to make the input cover a larger range. This combination is done by the `pbkdf2_hmac` so do not do it yourself.

To generate a salt, use the `os.urandom` function as it returns random bytes suitable for cryptographic use. This function does not use pseudo-random number generators so the return value is unpredictable; exactly what is required.

```python
import os

salt = os.urandom(32)
```

> 32 is the size returned in bytes. You can choose any size but I recommend making it over 16 bytes.

The output from this will be used in `pbkdf2_hmac` and then stored beside the output key (we will use it as a hash) from  `pbkdf2_hmac`. Every password relating to a user/entity must have its own hash, **do not use the same hash for all user's/entities passwords**.

### Hashing
Now that the basics of these concepts are out of the way, we can get down to executing some code. The best way to learn is by example and application, so here is an example:

```python
import hashlib
import os

salt = os.urandom(32) # Remember this
password = 'password123'

key = hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000 # It is recommended to use at least 100,000 iterations of SHA-256 
)
```

Since no key length was provided, the digest size of the hash algorithm is used; in this case, we use SHA-256 so the size will be 64 bytes. If you require a longer key for something like using this key in AES, pass the desired key size to `dklen` after the iteration in `hashlib.pbkdf2_hmac`; for example:

```python
import hashlib
import os

salt = os.urandom(32) # Remember this
password = 'password123'

key = hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000, # It is recommended to use at least 100,000 iterations of SHA-256 
    dklen=128 # Get a 128 byte key
)
```

> In these examples, the key is your "hash"

### Storing the Hash and Salt
From the snippets above, you need to store the salt and key. In terms of storage, you can use any method; JSON, SQL, CSV or even a raw text file. Make sure you do not store the password as that is the goal of all of this, not having to store the actual password.

If you are restricted to only one field for storage, you can add the salt and password together and then store them. When reading them out, you can then separate them as you know the length of the salt and key. For example:

```python
import os
import hashlib

# Example generation
salt = os.urandom(32)
key = hashlib.pbkdf2_hmac('sha256', 'mypassword'.encode('utf-8'), salt, 100000)

# Store them as:
storage = salt + key 

# Getting the values back out
salt_from_storage = storage[:32] # 32 is the length of the salt
key_from_storage = storage[32:]
```

> If it is possible to use two fields in your situation (most situations you can), then use two fields as it makes things less complicated

## Verification
After the user has supplied their password for the first time and you generated a salt for them, computed the key using the password and salt and then stored this password and salt, you can now check if further passwords are correct.

```python
import hashlib

salt = b'' # Get the salt you stored for *this* user
key = b'' # Get this users key calculated

password_to_check = 'password246' # The password provided by the user to check

# Use the exact same setup you used to generate the key, but this time put in the password to check
new_key = hashlib.pbkdf2_hmac(
    'sha256',
    password_to_check.encode('utf-8'), # Convert the password to bytes
    salt, 
    100000
)

if new_key == key:
    print('Password is correct')
else:
    print('Password is incorrect')
```

Regarding you used the snippet above to generate the first key, executing this should produce "Password is incorrect"; this is good because the passwords do not match. When running this again but with the correct password this time, the script should output "Password is correct" as the passwords match.

## Example of Adding a User and Verifying

```python
import hashlib
import os

users = {} # A simple demo storage

# Add a user
username = 'Brent' # The users username
password = 'mypassword' # The users password

salt = os.urandom(32) # A new salt for this user
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
users[username] = { # Store the salt and key
    'salt': salt,
    'key': key
}

# Verification attempt 1 (incorrect password)
username = 'Brent'
password = 'notmypassword'

salt = users[username]['salt'] # Get the salt
key = users[username]['key'] # Get the correct key
new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

assert key != new_key # The keys are not the same thus the passwords were not the same

# Verification attempt 2 (correct password)
username = 'Brent'
password = 'mypassword'

salt = users[username]['salt']
key = users[username]['key']
new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

assert key == new_key # The keys are the same thus the passwords were the same

# Adding a different user
username = 'Jarrod'
password = 'my$ecur3p@$$w0rd'

salt = os.urandom(32) # A new salt for this user
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
users[username] = {
    'salt': salt,
    'key': key
}

# Checking the other users password
username = 'Jarrod'
password = 'my$ecur3p@$$w0rd'

salt = users[username]['salt']
key = users[username]['key']
new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

assert key == new_key # The keys are the same thus the passwords were the same for this user also
```
