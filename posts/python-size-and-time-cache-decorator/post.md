title: "Python Size and Time Cache Decorator"
date: 2018-12-15
category: General
tags: [python, decorator]
feature: feature.png
description: "A Python decorator that allows developers to cache function return values and include expirations on remembered values."

[TOC]

## Introduction
Python's standard library comes with a memoization function in the `functools` module named [`@functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache). This can be very useful for pure functions *(functions that always will return the same output given an input)* as it can be used to speed up an application by remembering a return value. This is because next time a function is called with the same arguments, the value can be simply returned and computation will not have to occur again.

Sometimes though, you might want to remember the return value of a non-pure function for a specific amount of time. The function below is a decorator that allows you to remember return value but also have an expiry on them.

## Decorator
```python
def cache(size_limit=0, ttl=0, quick_key_access=False):
    def decorator(func):
        import time
        storage = {}
        ttls = {}
        keys = []

        def wrapper(*args, **kwargs):
            # Generate a key based on arguments being passed
            key = (*args,) + tuple([(k, v) for k, v in kwargs.items()])

            # Check if they return value is already known
            if key in storage:
                result = storage[key]
            else:
                # If not, get the result
                result = func(*args, **kwargs)
                storage[key] = result

                # If a ttl has been set, remember when it is going to expire
                if ttl != 0:
                    ttls[key] = time.time() + ttl

                # If quick_key_access is being used, remember the key
                if quick_key_access:
                    keys.append(key)

                # If a size limit has been set, make sure the size hasn't been exceeded
                if size_limit != 0 and len(storage) > size_limit:
                    if quick_key_access:
                        oldest_key = keys[0]
                        del keys[0]
                    else:
                        oldest_key = list(storage.keys())[0]
                    del storage[oldest_key]

            # Check ttls if it is enabled
            if ttl != 0:
                while True:
                    if quick_key_access:
                        oldest_key = keys[0]
                    else:
                        oldest_key = list(storage.keys())[0]

                    # If they key has expired, remove the entry and it's quick access key if quick_key_access=True
                    if ttls[oldest_key] < time.time():
                        del storage[oldest_key]
                        if quick_key_access:
                            del keys[0]
                    else:
                        break

            return result
        return wrapper
    return decorator
```

## Usage
To use this method, add it to your project/script. Then decorate your functions that you want to cache, for example:

```python
@cache
def my_sum(a, b, c, d=1, e=5):
    return a + b + c + d + e
```

Now when you call `my_sum(...)` values will be remembered and the addition will not have to occur each time. In this example, all the defaults are used which means it has unlimited storage (can be dangerous) and will live forever; this is the same as memoization will unlimited entries.

The first parameter for the `cache` function is called `size_limit`. This is the maximum amount of entries to be stored until values that have been stored for the longest are removed (only the oldest will be deleted in Python 3.7 and above due to the ordering of dictionaries). When this is set to `0`, there is no size limit.

`ttl` is the second parameter for this decorator. This is the number of seconds that each entry can exist for before it is removed from memory. When this is set to `0` entries will never expire.

There is also another parameter that can be passed called `quick_key_access`. When set to `true`, a lookup table is stored for each key that is generated. This is set to `false` by default but if you're remembering a lot of values, then this may help get a speed boost at the cost of taking up more space. Simply, when set to `false`, this is slower but will take up less space, when set to `true`, this is faster but will take up more space.

An example of using this decorator with a size limit of 10 cached entries, a time to live of 5min and using quick key access is shown below:

```python
@cache(10, 60 * 5, True)
def my_sum(a, b, c, d=1, e=5):
    return a + b + c + d + e
```

## Summary
If you want a simple memoization function, I still recommend using the built-in [`@functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache) decorator but if you are looking for memoization decorator with a time factor added in, then this is something that you're looking for.
