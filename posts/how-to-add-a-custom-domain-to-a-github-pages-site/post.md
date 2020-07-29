title: "How To Add a Custom Domain To a GitHub Pages Site"
date: 2018-04-29
category: Tutorials
tags: [website, domain]
feature: existing-resource-records.png
description: "In this tutorial, I explain how to configure your domain for GitHub Pages using a domain from Namesilo. You will first want to create a CNAME file for your GitHub pages site."

[TOC]

Yesterday night I purchased the domain [nitratine.net](https://nitratine.net/) from [Namesilo](https://www.namesilo.com/). There is a lot of help out there to set this up but unfortunately, there are no direct instructions for Namesilo specifically.

In this tutorial, I will explain how to configure your domain for GitHub Pages using a domain from Namesilo.

## Setting Up CNAME in GitHub
You will first want to create a CNAME file for your GitHub pages site. The easiest way to do this is to go to your project's repository and go to the settings tab on the right.

![GitHub Settings](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/github-settings.png)

Scroll down this page until you find the "GitHub Pages" block. In this block, there is a "Custom domain" header with an input field under it. In here put your domain you have registered.

![Custom Domain](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/custom-domain.png)

In this image, I have put "nitratine.net". This is where I want my site hosted. If you want your site hosted at www.example.com instead of example.com, put in www.example.com.

## Managing the DNS Records on Namesilo
Now that you have set up your CNAME, login to Namesilo and click my account at the top of the page. In the account overview block, click on the number beside "Account Domains".

![Account Overview](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/account-overview.png)

Now click on the blue globe button that corresponds with the domain you put in GitHub Pages.

![Domain Manager](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/domain-manager.png)

You should now be brought to the "Manage DNS" page. If not, try again. Now you have two paths depending on if you want www or not.

### WWW
GitHub's article on setting this up can be found [here](https://help.github.com/articles/setting-up-a-www-subdomain/) if you want a reference.

Setting up a www subdomain only requires one step. Click the "CNAME" link in the "Add/Edit a Resource Record" block.

![Add Resource Record](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/add-resource-record.png)

Now put "www" in the HOSTNAME input field and your current GitHub page URL into TARGET HOSTNAME. For example, I would put brentvollebregt.github.io in this as it is where by GitHub page is currently hosted. Leave TTL as it is and click submit.

![CNAME Record](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/cname-record.png)

This is all that needs to be done for a www subdomain. GitHub will decide what URL to use based on what you put in your Git repositories CNAME. You may have to wait a while until these entries are added by Namesilo but in my experience, it's very quick.

### No WWW
GitHub's article on setting this up can be found [here](https://help.github.com/articles/setting-up-an-apex-domain/) if you want a reference.

First you will need to add an A Record to 185.199.111.153. To do this click "A" in the "Add/Edit a Resource Record" grey box.

![Add Resource Record](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/add-resource-record.png)

In this, you want to insert `185.199.111.153` into "IPV4 ADDRESS" but leave the hostname field blank. You can leave the TTL as it is and click submit.

![First IP](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/first-ip.png)

Now repeat this another three times and use the IP addresses: `185.199.110.153`, `185.199.109.153` and `185.199.108.153`

After that, we will set up the www routing by clicking "CNAME" in the grey box. In here, add www to the HOSTNAME field and your current GitHub pages address to TARGET HOSTNAME. For example, I would put brentvollebregt.github.io in this as it is where by GitHub page is currently hosted. Leave the TTL the same again and click submit. If you are confused about this look under the WWW sub-heading for how to do this.

> You do not have to add a www in this situation but I feel it is good to have www.example.com and example.com point to the same place for consistency.

You should now have five entries in the "Existing Resource Records" (4 A records and 1 CNAME).

![Existing Resource Records](/posts/how-to-add-a-custom-domain-to-a-github-pages-site/existing-resource-records.png)

GitHub will decide what URL to use based on what you put in your git repositories CNAME. You may have to wait a while until these entries are added by Namesilo but in my experience, it's very quick.

## SSL (Green Padlock)
Following these steps and using the new IP addresses, you will now be provided SSL for free from Github with no extra effort.

If this did not occur (it didn't work the first time I tried), go to the git repo on Github and then go to settings. Scroll down this page until you find the "GitHub Pages" block. In this block, there is a "Custom domain" header with an input field under it (just like we did in Setting Up CNAME in GitHub). Clear this field and click save. Now put your URL in the input field (the one you just cleared) and save it. This reset of the URL can trigger the SSL certificate generation and you should get SSL on your website in under a day.

## Sub Domains
Sometimes when having your domain `example.com` point to your main site, you may also want `subdomain1.example.com` to point to a different site and `subdomain2.example.com` point to yet another. This is a lot easier to do as it seems; first add a CNAME file to the GitHub repository you are going to use, for example, `subdomain1.example.com`, to set up the domain on GitHub's side.

Next, you'll want to go back to the "Manage DNS" page we have been using previously (may be different on other domain register sites) and add a new CNAME record like in the www tutorial above. Now in the hostname field, instead of www, add `subdomain1` and put your GitHub pages URL in the target hostname (mine is brentvollebregt.github.io).

Now wait for changes to be applied to the DNS and you can now visit `subdomain1.example.com` to visit your new site.
