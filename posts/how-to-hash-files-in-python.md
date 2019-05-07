title: "How to Hash Files in Python"
date: 2019-05-07
category: Tutorials
tags: [python]
feature: feature.png
description: "Hashing files allows us to generate a string/byte sequence that can help identify a file. This can then be used by comparing the hashes of two or more files to see if these files are the same as well as other applications."

[TOC]

> Note: This post assumes you already know what a hash is, if you don't, read up on hashes before reading this post. Sites like [this](https://cs.stackexchange.com/a/55472) or [this](https://stackoverflow.com/a/506035) can help you out. 

## What Does it Mean to Hash a File?
Hashing a file is when a file of arbitrary size is read and used in a function to compute a fixed-length value from it. This fixed length value can help us get a sort of 'id' of a file which can then help us do particular tasks (examples follow).

Strong hashes with large amounts of bytes can help distinguish between many different files, but we do always need to remember the [birthday problem](https://en.wikipedia.org/wiki/Birthday_problem). For example, the birthday problem reminds us that if we have a 160bit hash, there can only be 2^160 different hashes, meaning that as soon as we generate 2^160 + 1 hashes of different files, it is guaranteed that we find a duplicate hash. This duplicate hash means we get the same hash for different files which can cause issues in some applications.

### What Can I Do With A File Hash?
File hashes are quite useful as they can represent (not substitute) a file, meaning that you do not have to store the whole file when trying to identify a file. When hashing files (or anything in general), you will get the same result hash result every time you hash a particular file. This makes hashing files useful for things like:

 - **Comparing files**: Instead of comparing whole files, take hashes and compare hashes together. This is particularly efficient when comparing more than one file to another file.
 - **Easily identifying files without storing the whole file**: If you are looking for a file, simply get the hash of your current file and hash other files as you look at them while looking for a match. This technique is used by some anti-virus software.
 - **Stopping filename clashes**: Rename files where many files are located in one directory to their hash. This will mean two different files will not have the same name and will save on space when two files have the same name as they will overwrite (does not work if you need two of the same file).
 - **Object keys**: Just like in the point "Stopping filename clashes", using hashes as object keys can help identify what objects match to which file.
 - **Detecting changes in a file**: If you had a file hash before it was modified, you can re-hash the file and compare it against the original hash to see if it has been modified.

#### What Can I Not Do With A File Hash?
Even though you can compute a hash using a file, this does not mean you cannot get the original file back using this hash. Hashing is a one way function (lossy) and is not an encryption scheme.

## Supported Hashing Algorithms in Python
The [`hashlib` Python module](https://docs.python.org/3/library/hashlib.html) *"implements a common interface to many different secure hash and message digest algorithms"*. To look at the hashing algorithms Python offers, execute:

```python
import hashlib
print(hashlib.algorithms_guaranteed)
```

This will print a set of strings that are hash algorithms guaranteed to be supported by this module on all platforms. To use these, select a hashing algorithm from the set and then use it as shown below (this example uses sha256):

```python
import hashlib
h = hashlib.sha256() # Construct a hash object using our selected hashing algorithm
h.update('My content'.encode('utf-8')) # Upade the hash using a bytes object
print(h.hexdigest()) # Print the hash value as a hex string
print(h.digest()) # Print the hash value as a bytes object
```

### hashlib.algorithms_guaranteed vs hashlib.algorithms_available
To get all the algorithms available in your interpreter, you can execute `hashlib.algorithms_available`. Unlike the output from `hashlib.algorithms_guaranteed`, these hashes aren't guaranteed to exist in interpreters on other machines. You can [visit the docs](https://docs.python.org/3/library/hashlib.html#hashlib.algorithms_guaranteed) to get more information on this.

## Hashing a File
To hash a file, read it in bit-by-bit and update the current hashing functions instance. When all bytes have been given to the hashing function in order, we can then get the hex digest.

```python
import hashlib

file = ".\myfile.txt" # Location of the file (can be set a different way)
BLOCK_SIZE = 65536 # The size of each read from the file

file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
with open(file, 'rb') as f: # Open the file to read it's bytes
    fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
    while len(fb) > 0: # While there is still data being read from the file
        file_hash.update(fb) # Update the hash
        fb = f.read(BLOCK_SIZE) # Read the next block from the file
        
print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash
```

This snippet will print the hash value of the file specified in `file` generated using the SHA256 algorithm. The call `.hexdigest()` returns a string object containing only hexadecimal digits; you can use `.digest()` as shown before to get the bytes representation of the hash.

### Why do I Need to Worry About the Buffer Size?
You would have noticed in the script above, the variable `BLOCK_SIZE` is set to `65536`. This is the amount of bytes that is read into memory in a single read operation. This is used so larger files are not completely loaded into memory before computing the hash. 

For example, if we did not do this and were hashing a video file that was 2Gb large, the whole 2Gb file would be loaded into memory (or at least tried to) and then hashed. This approach reads the file block-by-block so we don't load the whole file into memory.

The buffer I have used is 64Kb but you can use any value you wish. Making this larger reads files faster, but in turn loads more of the file into memory at once.
