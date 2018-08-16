---
layout: page
permalink: /data/
title: "Data"
description: "A place where you can see view counts for all my pages, GitHub repo stats and other numbers related to the work I do. Always up to date."
---

* content
{:toc}

This post is a place where you can see view counts for all my pages, GitHub repo stats and other numbers related to the work I do.

## Post View Counts
These counts are counted using [hitcounter.pythonanywhere.com](https://hitcounter.pythonanywhere.com). They are not 100% accurate but will be a reasonable idea of the actual views (better than Google Analytics being blocked by ad-blockers)

<table>
	<thead>
		<tr>
			<th>Post</th>
			<th>Hits</th>
		</tr>
	</thead>
	<tbody>
	    {%- for post in site.posts -%}
		<tr>
			<td><a href="{{ post.url }}">{{ post.title }}</a></td>
			<td><script>document.write('<img src="https://hitcounter.pythonanywhere.com/nocount/tag.svg?url=' + encodeURIComponent("{{ site.url }}{{ post.url }}") + '" alt="Hits" style="margin-bottom: -4px;">')</script></td>
		</tr>
		{%- endfor -%}
	</tbody>
</table>

{%- if site.github.public_repositories != null -%}
{%- assign repos = site.github.public_repositories | sort: "stargazers_count" | reverse -%}
## GitHub Repository Stats
As uneventful some of my repositories are, I'm always curious if there is any action on them.

<table>
	<thead>
		<tr>
			<th>Repository</th>
			<th>Stars</th>
			<th>Forks</th>
			<th>Watchers</th>
		</tr>
	</thead>
	<tbody>
	    {%- for repository in repos -%}
		<tr>
			<td><a href="https://github.com/brentvollebregt/{{ repository.name }}">{{ repository.name }}</a></td>
			<td><img src="https://img.shields.io/github/stars/{{ repository.owner.login }}/{{ repository.name }}.svg?style=social" alt="Stars" style="margin-bottom: -5px; display: inline-block;"></td>
			<td><img src="https://img.shields.io/github/forks/{{ repository.owner.login }}/{{ repository.name }}.svg?style=social" alt="Forks" style="margin-bottom: -5px; display: inline-block;"></td>
			<td><img src="https://img.shields.io/github/watchers/{{ repository.owner.login }}/{{ repository.name }}.svg?style=social" alt="Watchers" style="margin-bottom: -5px; display: inline-block;"></td>
		</tr>
		{%- endfor -%}
	</tbody>
</table>
{%- endif -%}

## Other

<table>
	<thead>
		<tr>
			<th>Post</th>
			<th>Hits</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>YouTube Subscribers (rounded)</td>
			<td><script src="https://apis.google.com/js/platform.js" gapi_processed="true"></script><div class="g-ytsubscribe" data-channel="PrivateSplat" data-layout="default" data-count="default"></div></td>
		</tr>
		<tr>
			<td>GitHub Followers</td>
			<td><img src="https://img.shields.io/github/followers/brentvollebregt.svg?style=social" alt="GitHub Followers"></td>
		</tr>
		<tr>
			<td>Twitter Followers</td>
			<td><img src="https://img.shields.io/twitter/follow/pytutorials.svg?style=social" alt="Twitter Followers"></td>
		</tr>
	</tbody>
</table>
