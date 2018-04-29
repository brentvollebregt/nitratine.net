---
layout: post
title: "How To Add a Custom Domain To a GitHub Pages Site"
date: 2018-04-25
categories: Tutorials
tags: Website Domain
---

* content
{:toc}

Yesterday night I purchased the domain [nitratine.net](http://nitratine.net/) from [Namesilo](https://www.namesilo.com/). There is a lot of help out there to set this up but unfortunately there is no direct instructions for Namesilo specifically.

In this tutorial I will explain how to configure your domain for GitHub Pages using a domain from Namesilo.

## Setting Up CNAME in GitHub
You will first want to create a CNAME file for your GitHub pages site. The easiest way to do this is to go to your projects repository and go to the settings tab on the right.

![GitHub Settings](/images/how-to-add-a-custom-domain-to-a-github-pages-site/github-settings.png)

Scroll down this page until you find the "GitHub Pages" block. In this block, there is a "Custom domain" header with an input field under it. In here put your domain you have registered.

![Custom Domain](/images/how-to-add-a-custom-domain-to-a-github-pages-site/custom-domain.png)

In this image I have put "nitratine.net". This is where I want my site hosted. If you want your site hosted at www.example.com instead of example.com, put in www.example.com.

## Managing the DNS Records on Namesilo
Now that you have set up your CNAME, login to Namesilo and click my account at the top of the page. In the account overview block, click on the number beside "Account Domains".

![Account Overview](/images/how-to-add-a-custom-domain-to-a-github-pages-site/account-overview.png)

Now click on the blue globe button that corresponds with the domain you put in GitHub Pages.

![Domain Manager](/images/how-to-add-a-custom-domain-to-a-github-pages-site/domain-manager.png)

You should now be brought to the "Manage DNS" page. If not, try again. Now you have two paths depending if you want www or not.

### WWW
GitHubs article on setting this up can be found [here](https://help.github.com/articles/setting-up-a-www-subdomain/) if you want reference.

Setting up a www subdomain only requires one step. Click the "CNAME" link in the "Add/Edit a Resource Record" block.

![Add Resource Record](/images/how-to-add-a-custom-domain-to-a-github-pages-site/add-resource-record.png)

Now put "www" in the HOSTNAME input field and your current GitHub page url into TARGET HOSTNAME. For example I would put brentvollebregt.github.io in this as it is where by GitHub page is currently hosted. Leave TTL as it is and click submit.

![CNAME Record](/images/how-to-add-a-custom-domain-to-a-github-pages-site/cname-record.png)

This is all that needs to be done for a www subdomain. GitHub will decided what url to use based on what you put in your Git repositories CNAME. You may have to wait a while until these entries are added by Namesilo but in my experience it is very quick.

### No WWW
GitHubs article on setting this up can be found [here](https://help.github.com/articles/setting-up-an-apex-domain/) if you want reference.

My site doesn't use www so I made it so that www is still routed to nitratine.net. To do this click "A" in the "Add/Edit a Resource Record" grey box.

![Add Resource Record](/images/how-to-add-a-custom-domain-to-a-github-pages-site/add-resource-record.png)

In this you want to insert `192.30.252.153` into "IPV4 ADDRESS" but leave the hostname field blank. You can leave the TTL as it is and click submit.

![First IP](/images/how-to-add-a-custom-domain-to-a-github-pages-site/first-ip.png)

Now do this again but this time put the ip address `192.30.252.154` in.

After that we will set up the www routing by clicking "CNAME" in the grey box. In here, add www to the HOSTNAME field and your current GitHub pages address to TARGET HOSTNAME. For example I would put brentvollebregt.github.io in this as it is where by GitHub page is currently hosted. Leave the TTL the same again and click submit.

You should now have three entries in the "Existing Resource Records".

![Existing Resource Records](/images/how-to-add-a-custom-domain-to-a-github-pages-site/existing-resource-records.png)

GitHub will decided what url to use based on what you put in your Git repositories CNAME. You may have to wait a while until these entries are added by Namesilo but in my experience it is very quick.
