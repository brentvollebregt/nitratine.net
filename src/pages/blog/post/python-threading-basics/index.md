---
templateKey: blog-post
title: "Python Threading Basics"
date: 2018-05-03T12:00:00.000Z
category: YouTube
tags: [python, threading]
image: feature.png
description: "This post covers the basics of Python's threading module. Threading allows you to run multiple tasks at the same time. This allows you to do one or more tasks while another task runs."
disableToc: false
hidden: false
---

<youtube-video id="5JSloPGocSY"></youtube-video>

## What is Threading?

The threading module comes pre-installed with python so there are no downloads or installs for this tutorial. Threading allows us to call a method or class that has extended the `threading.Thread` class to run alongside the main thread (the linear flow that generally happens).

One good use of threading is to create multiple instances of things that take time outside your program. A great example of this is sending requests to a server. If you want to send many, instead of waiting for them to finish one-by-one before you send the next request, you can create many threads to request different URLs and they will then all be waiting at the same time.

## Threading a Method

A basic example of threading can be seen below:

```python
import threading

def worker():
    print ('Hello World\n') # Add \n so a newline is forced

thread_list = []
for i in range(4):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)
    thread.start()
```

In this example, we create a place to store the threads and then loop 4 times as we create the threads. To create the threads, we first initialise a threading.Thread instance passing the method as the target. We then add this thread to our previously create list and start it. This will provide the following output:

```console
$ python threading_method.py

Hello World
Hello World
Hello World
Hello World
```

Note that there are no brackets after worker when defining the target. This is because we need to pass the method, not what the method returns (even if it returns nothing).

### Passing Arguments

To pass arguments to a method when creating the thread, we can pass a tuple to args. For example:

```python
import threading

def worker(number):
    print ('I am thread: ' + str(number) + '\n')

thread_list = []
for i in range(4):
    thread = threading.Thread(target=worker, args=(i,))
    thread_list.append(thread)
    thread.start()
```

In this expanded example I have added a number parameter to `worker` which will then be used in the output. When creating the instance of threading.Thread, I pass the `i` variable to `args` in a tuple. This will provide the output:

```console
$ python threading_method_args.py

I am thread: 0
I am thread: 1
I am thread: 2
I am thread: 3
```

The reason args is set to `(i,)` and not `(i)` is because if we left out the comma, the type would no longer be a tuple and would cause an error.

## Threading a Class

Threading a class can be quite useful as you can have many methods particular to a thread and it's easier to keep your data in one place specific to a thread. An example of threading a class is:

```python
import threading

class MyThread(threading.Thread):
	def __init__(self):
		super(MyThread, self).__init__()
		# Can setup other things before the thread starts
	def run(self):
		print ("Running")

thread_list = []
for i in range(4):
    thread = MyThread()
    thread_list.append(thread)
    thread.start()
```

In this example, I create a class that extends threading.Thread. I have created the initialisation method with an initialisation call to the super class and a **run method which is what will be run when I call start()**. Just like last time I loop 4 times but this time I only need to use `MyThread()` to set up the thread variable. This will provide the output:

```console
RunningRunningRunningRunning



```

See how all the strings are together; this shows that they were all printed at very similar times and then all the new lines were put in. In the above examples, this did not occur as I force the newline character.

Note that if you do not need an initialisation method, you can remove it completely including the super() call.

### Passing Arguments

To pass arguments, you just use the class as you would normally. For example:

```python
import threading

class MyThread(threading.Thread):
	def __init__(self, number):
		super(MyThread, self).__init__()
		self.number = number
	def run(self):
		print (self.number)

thread_list = []
for i in range(4):
    thread = MyThread(i)
    thread_list.append(thread)
    thread.start()
```

In this example, I had added a parameter to the class in the initialisation method like you normally would and saved it so it can print it later. Then I simply passed a variable to the class which will be printed. This will output:

```console
0123



```

Just like last time they concatenated into one string followed by new line characters. When passing variables you need to keep the super() call as you are now using the initialisation method unless you pass it in with a different method before calling run.

## Managing Your Threads

Python has a lot of useful methods, variables and parameter to manage your threads. These are some of the basic ones.

### Naming

Setting names for threads can be quite useful for identifying them. To do this, when creating a thread call `.setName()` and pass a string. For example:

```python
thread = MyThread()
thread.setName('MyThread 1')
thread.start()
```

Now to get the name of the thread just call `.getName()` on the thread object. There are a few ways of getting the thread object depending on how you stored it. If you are inside the thread and you're in a threading class, you can just use `self`; for example:

```python
class MyThread(threading.Thread):
	def __init__(self):
		super(MyThread, self).__init__()
    def run(self):
        print (self.getName())
```

If you want to get it outside of the class, you can just get the variable you saved it under and use that. For example, when I saved the threads in a list before, I can just use an element from it as they are the threading objects I want. The following example will print the name of the first thread added to this list.

```python
thread_list = []
for i in range(4):
    thread = MyThread(i)
    thread.setName('MyThread ' + str(i))
    thread_list.append(thread)
    thread.start()
print (thread_list[0].getName())
```

### Joining Threads

Joining a thread allow us to wait until it is terminated before we carry on. For example:

```python
import threading

class MyThread(threading.Thread):
	def __init__(self):
		super(MyThread, self).__init__()
	def run(self):
		print ("Running")

thread = MyThread()
thread.start()
thread.join()
print ("Thread has finished")
```

In this example, I create the thread and start it. I then call join which waits until the thread is finished. If the thread called does not finish, the thread that called the `.join()` method (can be the main thread) will wait indefinitely. This means that you shouldn't use .join() on threads that don't finish unless you want to stop the execution of the thread for another reason.

You can wait for many threads to finish by calling .join() after you started them all. The following example will wait until all 4 threads are finished before it goes to the print statement.

```python
import threading

class MyThread(threading.Thread):
	def __init__(self):
		super(MyThread, self).__init__()
		# Can setup other things before the thread starts
	def run(self):
		print ("Running")

thread_list = []
for i in range(4):
    thread = MyThread()
    thread_list.append(thread)
    thread.start()

for thread in thread_list:
    thread.join()
print ("Thread has finished")
```

### Daemon Threads

A daemon thread is a thread that will not keep running if the rest of the script has stopped and there are no more non-daemon threads left. We can tell the main thread is non-daemon as it is not abruptly stopped when it's the only thread running.

This means setting a threads daemon value to `True` will mean that it will not keep running after the main thread has finished (or other non-daemon threads); we can set `daemon` to `False` to make sure the thread keeps running even when the main thread finishes. The daemon value must be set before `.start()` is called on the thread. To set if a thread is daemon, you can pass `daemon=True` (or `False`) in the same place I put args before:

```python
thread = threading.Thread(target=worker, args=(i,), daemon=True)
```

You can alternatively set a thread to be daemon using `.daemon = bool` on the thread. If you are threading a class, you can call `self.daemon = bool` in the initialisation method or `.daemon = bool` on the thread like if you were threading a method. For example:

```python
thread = MyThread()
thread.daemon = True
thread.start()
```

To check if a thread is daemon, you can check `.daemon` on the thread; this is a bool.

### Getting All Threads

If you want to get all the threads that are currently alive, you can call `threading.enumerate()`. This will return all alive threads including the main thread in a list. If you want to get all the names of the current alive threads, use:

```python
for thread in threading.enumerate():
    print (thread.getName())
```

### Is a Thread Alive?

If you want to check if a particular thread is still alive, you can call `.is_alive()` on the thread. This will return true if the thread is still running.

## Why it Won't Make Your Script Run Faster

In most cases, threading your pre-existing code will not make it run any faster. Python threads are designed to run multiple tasks at the same time, however, this is only on one CPU core.

A normal python script is run on a single core so when you create threads it will not speed up as it is basically doing the same thing just at different times. This issue/feature (if you want to look at it in a positive way) is due to the [Global Interpreter Lock](https://stackoverflow.com/questions/1294382/what-is-a-global-interpreter-lock-gil) which in short means that "multiple threads can't effectively make use of multiple cores" which is the reason for no speed increase. [Here](https://www.youtube.com/watch?v=ph374fJqFPE) is a great talk on the GIL with [some great slides](http://www.dabeaz.com/python/GIL.pdf).

If you do want to have multiple tasks running on multiple cores, look at the [multiprocessing module](https://docs.python.org/3.4/library/multiprocessing.html).

## Extra Resources

Since this is only a basic look over threading so someone that hasn't used it can understand it better, I have left out things like events, signalling and locks. To read more about threads, you could visit these pages:

- [pymotw.com/3/threading/](https://pymotw.com/3/threading/)
- [Python 3 Threading Documentation](https://docs.python.org/3/library/threading.html)
