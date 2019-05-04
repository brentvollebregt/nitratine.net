title: "How to Hash Files in Python"
date: 2019-04-24
category: Tutorials
tags: [python]
feature: feature.png
description: "Hashing files and strings have many useful Hashing files can be helpful for easily checking if two files are identical "

[TOC]

## What Does it Mean to Hash a File?
Hashing a file is when a file is read and used in a function to compute a fixed-length value from it. This fixed length value is different

- "A hash function is any function that can be used to map data of arbitrary size onto data of a fixed size." 
- "A "hash" is a function h referred to as hash function that takes as input objects and outputs a string or number."
- You can make your own easy
- The main properties that a hash function should have are:
    - It should be easy to compute
    - The outputs should be relatively small

### Why are Hashes Useful?
- Easily identify files without storing the whole file
- Irreversible functions for things like password storage
- Object keys (data storage buckets)
- These won't change each time you run it

## Supported Hashing Algorithms in Python
```python
import hashlib
hashlib.algorithms_guaranteed
```

### hashlib.algorithms_guaranteed vs hashlib.algorithms_available
- Difference
- https://docs.python.org/3/library/hashlib.html#hashlib.algorithms_guaranteed

## Hashing a File
- Code to hash a file
```python
import hashlib

file = ".\myfile.txt"
BLOCK_SIZE = 65536

file_hash = hashlib.sha256()
with open(file, 'rb') as f:
    fb = f.read(BLOCK_SIZE)
    while len(fb) > 0:
        file_hash.update(fb)
        fb = f.read(BLOCK_SIZE)
        
print (file_hash.hexdigest())
```

- .digest to get bytes
- .hex digest to get a string object of double length, containing only hexadecimal digits. This may be used to exchange the value safely in email or other non-binary environments.

### Why do I Need to Worry About the Buffer Size?
- Don't want to dump a movie in memory

## Further Reading
- [Stackoverflow: What exactly (and precisely) is “hash?”](https://cs.stackexchange.com/a/55472)

