title: "How to Hash Files in Python"
date: 2019-04-24
category: Tutorials
tags: [python]
feature: feature.png
description: ""

[TOC]

## What Does it Mean to Hash a File in Python?
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

## Why do I Need to Worry About the Buffer Size?
- Don't want to dump a movie in memory

## Further Reading
- [Stackoverflow: What exactly (and precisely) is “hash?”](https://cs.stackexchange.com/a/55472)

