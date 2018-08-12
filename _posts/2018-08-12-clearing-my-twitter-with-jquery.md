---
layout: post
title: "Clearing My Twitter with jQuery"
date: 2018-08-12
categories: General
tags: Twitter JavaScript jQuery API tweepy
description: ""
---

* content
{:toc}

A while ago I had decided that I would want to keep my Twitter handle that I used for my bot, so I needed to remove all the re-tweets, follows and liked tweets from this account. One option was to create a new account under a different email and move the handle over, but I wanted to keep the handle under the email address it is currently under so that was not an option.

I then decided to use a bulk tweet deleter tool online to delete tweets on my account; unfortunately this has "broken" my twitter account. There are tweets I have re-tweeted that I can not un-re-tweet and the counts for Tweets and Likes on my profile are now way out.

This article will go over how I used jQuery on twitter.com to get rid of the tweets I still could access and unfollow people in bulk. I was not able to delete everything as I have lost access to some tweets but this got rid of quite a few and I feel this method would work if you haven't used a bulk tool.

<!-- more -->

## Unfollowing Accounts
I first wanted to remove all the users my bot followed. Going into the ["Following"](https://twitter.com/following) tab in twitter shows everyone you have followed with blue buttons that go red and change text to "Unfollow" when you hover on them.

![Unfollow Button](/images/clearing-my-twitter-with-jquery/unfollow_btn.png)

My idea for this was to simulate clicking each of these buttons for every user I followed. Thankfully, Twitter uses jQuery so I could use some very simple methods for finding each tile and then clicking on them using ```.click()```.

Looking at the source, all these tiles were in a div with a class of 'GridTimeline-items' which was the only tag with this class. A simple call of ```$.find('.GridTimeline-items')[0]``` allowed me to get this. If I didn't get only the tiles in this class, I would be finding follow buttons on the left which when clicked would follow them.

Next I needed to get all the buttons which all had a class of 'unfollow-text'. Once again I could call ```.find('.unfollow-text')``` to get all the instances of the class. So to find all the buttons, I can concatenate them to form ```$($.find('.GridTimeline-items')[0]).find('.unfollow-text')``` which will return all the buttons in a list that relate to all the users I follow.

![Unfollow Button](/images/clearing-my-twitter-with-jquery/followers.png)

Simply looping through this list and clicking the buttons now made all the people I followed disappear.

```javascript
function clickUnfollow() {
    buttons = $($.find('.GridTimeline-items')[0]).find('.unfollow-text')
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].click();
        console.log(i)
    }
}
```

Calling the method ```clickUnfollow()``` quickly clicks all the unfollow buttons of users I follow.

## This Didn't Unfollow Everyone?
Originally I forgot that this will only unfollow the users that are rendered on the page currently, so I had to find a way to put everyone on one page (or at least a lot more of them) to make the process a lot easier and less repetitive.

A way to fix this was to make something to automatically scroll down for me so users could be rendered when the requests were made to Twitter to show me more of my followers. (Basically: put my users on my following page)

I first created a simple sleep method thanks to [this answer](https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep), this would allow me to sleep in between each scroll down to give Twitter some time to send my followers to me (the request to be fulfilled).

```javascript
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

Then I needed to scroll down and use this sleep method. A simple for loop that sleeps, [scrolls to the bottom](https://stackoverflow.com/questions/4249353/jquery-scroll-to-bottom-of-the-page) using ```.animate()``` and prints where it is currently was easy to create:

```javascript
async function scroll() {
    for (var i = 0; i < 100; i++) {
        await sleep(1000);
        $("html, body").animate({ scrollTop: $(document).height()-$(window).height() });
        console.log(i);
    }
}
```

Now when you execute ```scroll()```, the page will be scrolled down for 100 seconds trying to load people I follow, it will log where it currently is. When this is complete, run ```clickUnfollow()``` again to unfollow all the users shown. Reload the page and repeat until you have no more.

This may not be the most efficient way but the time and effort still in this method was a great trade off for how easy it was. Added bonus: you don't have to authorise some third-party app.

## Unlike All of my Liked Tweets
Next was to unlike all of the tweets my bot had liked. Going to the ["Likes"](https://twitter.com/i/likes) tab, it is clear to see in Chromes DevTools that I need to click on buttons with the class 'ProfileTweet-action--unfavorite'. A simple find once again will find all of these: ```$.find('.ProfileTweet-action--unfavorite')```.

Just like last time, you will need to implement the scroll functions to load some more liked posts so they can be deleted in larger bunches. Looping over the result from the find query before and clicking each button will unlike the post.

```javascript
function unlike() {
    a = $.find('.ProfileTweet-action--unfavorite')
    for (var i = 0; i < a.length; i++) {
        a[i].click();
        console.log(i)
    }
}
```

Once again, scroll to the button, then call ```unlike```. When everything has been unliked (you will see the bottom tile is unliked) then reload and redo until they are all gone.

> Make sure to re-create the methods on each page load as they will disappear. Simply using the up arrow in Chrome DevTools' console will revise previous statements.

## Removing Retweets
Removing retweets got a bit tricky but there was a pattern. Looking for all elements with the class 'ProfileTweet-actionButtonUndo' and 'js-actionRetweet' on your profile will return all the green 'retweet' buttons; using the querySelectorAll method can do this: ```document.querySelectorAll('.ProfileTweet-actionButtonUndo.js-actionRetweet')```.

Unfortunately for tweets that you haven't retweeted that are on your profile (like tweets by you) also have these buttons, they are just hidden. To filter out these hidden nodes, loop over each of the nodes returned and get the style display value using ```.css('display')``` provided in jQuery; make sure you wrap the node in $() for this to work.

If the node we get is being displayed, then we need to click it. Else if we are returned 'none' then we need to ignore it.

```javascript
function unretweet() {
    var nodes = document.querySelectorAll('.ProfileTweet-actionButtonUndo.js-actionRetweet');
    for (var i = 0; i < nodes.length; i++) {
        if ( !$(nodes[i]).css('display') === 'none' ) {
            $(nodes[i]).click();
        }
    }
}
```

Like previous, you can load th page using the scroll methods and then run this method by calling ```unretweet()```.

## Trying to Access Tweets Over Twitters API
For those that haven't used bulk tweet-deleters before, the above methods probably worked; for me it didn't because I had used a bulk tweet-deleter. The final plan I had was to delete retweets them using the API.

To start this method off, create a new twitter app (or even use an existing if you want) at [apps.twitter.com](https://apps.twitter.com/). Get all your keys/tokens/secrets and create a new Python file. You will need tweepy installed which can be simply achieved using ```python -m pip install tweepy```. In that file created, import tweepy, set your keys/tokens/secrets to variables and then authorise the script.

```python
import tweepy

# Fill in the strings for these variables
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

```

Running this script should end gracefully, no errors. If there are errors, search them up; I'm sure StackOverflow will have an answer.

We now need to find the id of the re-tweet we want to delete. Go back into ChromeDev Tools on your twitter timeline and select a tweet you want to un-retweet. You might be thinking "why can't I just click the (now green) retweet button to un-retweet?". That is because the function literally just doesn't work in browser anymore, I have no clue why; twitter is broken. When you look at the tweet in the Elements tab, go up the tree until you find the div related to this tweet with a class 'tweet'*[]:

An easier way to find this would be to execute ```$.find('.tweet')``` in the Console tab, expand the results and then hover over each item until it highlights your tweet; when it does highlight the tweet you are aiming for, click on it to be shown it in the Elements tab.

Now that we are looking at the correct node, you will see it has a lot of attributes. The *data-tweet-id* is the id of who originally tweeted and the *data-retweet-id* attribute is the id of who retweeted (hopefully you). Copy the value related to *data-retweet-id* (will be a large number) and set it to a variable in your script as a string. We can now call ```api.get_status(id)``` to get info about this tweet, you can use this to verify it is the correct tweet if you want.

Finally, you will wan to call ```api.destroy_status(id)``` to murder the re-tweet (or even tweet if you are using this method to delete a tweet you created). Technically, if you own the tweet, as in if you were the one that retweeted, it should delete.

```python
import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

id = '1019797124492349441' # data-retweet-id

# api.get_status(id) Can use this if you want to look at the tweet
api.destroy_status(id)
```

For the tweets I could see when logged in, this method removed them.

Interestingly, when removing the tweets I could only see when not logged in, I was getting an error stating *"You have been blocked from the author of this tweet"* when calling ```api.get_status(id)```. When not bothering to check them and just calling ```api.destroy_status(id)``` they were being deleted. How is this even possible?

```api.destroy_status(id)``` actually returns a *Status* object which I investigated in PyCharm's Debug console. Looking at ```Status.author.name``` it clearly stated that I (PyTutorials) was the author; what a joke.

## Conclusion

So in the end I was able to delete all of the visible tweets both when logged in and out. My tweet count is still sitting at about 2.5k but none of these are being received (do they even exist?). I was successful in what I set out to do and definitely recommend this method to others.

This method may be a bit more time consuming but copying and pasting the code from here will be a lot better in the long run than having locked tweets that you have to forcefully delete using the API and then have incorrect tweet counts.
