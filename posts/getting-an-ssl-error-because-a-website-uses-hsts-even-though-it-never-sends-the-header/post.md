title: "Getting an SSL error because a website uses HSTS even though it never sends the header?"
date: 2024-02-24
category: General
tags: [ssl, website]
feature: ssl-warning-no-domain.png
description: "Recently I was getting an SSL warning that I could not ignore because Chrome said my site was setting HSTS even though it never set the Strict-Transport-Security header."

[TOC]

## Problem

Recently, I was setting up a subdomain of mine to point to a service running on my Raspberry Pi. After setting up Nginx and SSL, I visited the site and got an SSL error saying "Your connection is not private" NET::ERR_CERT_COMMON_NAME_INVALID. This was expected as I was using a self-signed certificate, so I clicked "Advanced" and expected to see a "Proceed to subdomain.example.com (unsafe)" link.

Unexpectedly, I did not see the "Proceed to subdomain.example.com (unsafe)" link available and instead saw the following message:

[![SSL warning](/posts/getting-an-ssl-error-because-a-website-uses-hsts-even-though-it-never-sends-the-header/ssl-warning-no-domain.png)](/posts/getting-an-ssl-error-because-a-website-uses-hsts-even-though-it-never-sends-the-header/ssl-warning-no-domain.png)

> You cannot visit subdomain.example.com right now because the website uses HSTS. Network errors and attacks are usually temporary, so this page will probably work later.

Looking at the request using Chrome DevTools, I was unable to see the header "Strict-Transport-Security" set. So even though Chrome was saying I could not ignore the SSL error since it was returning an HSTS header, my site was not returning an HSTS header - what???

## Potential Solution

After a lot of looking around, I had a hunch that my site at example.com had something to do with this - it was a public-facing website hosted using Azure Static Web Apps. Looking at the headers for example.com, I saw the following header,

> Strict-Transport-Security: max-age=10886400; includeSubDomains; preload

I had never set this header manually; it seems that Azure Static Web Apps had set it automatically. That `includeSubDomains` directive looked awfully suspicious and after [a quick search](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security#includesubdomains), I concluded this was my issue,

> includeSubDomains (optional): If this optional parameter is specified, this rule applies to all of the site's subdomains as well.

The way to fix my issue was to remove `includeSubDomains` (and also `preload` since it requires `includeSubDomains`).

After removing `includeSubDomains` from the "Strict-Transport-Security" header, I had to go back to example.com and do a hard reload before being able to use subdomain.example.com again. This was because I needed my browser to recognise that example.com no longer had `includeSubDomains` in the header so it would no longer apply to the subdomain.


### My Fix in Azure Static Web Apps

While your issue may be different, if you are using Azure Static Web Apps, this was my fix,

```json
{
  "globalHeaders": {
    "Strict-Transport-Security": "max-age=10886400"
  }
}
```

10886400 was the default max-age Azure Static Web Apps set, but this is recommended to be 2 years.