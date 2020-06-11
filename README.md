# ericmjalbert.github.io

This is my personal website, mainly meant to act as a professional portfolio and log of my side projects.

## Overview

The blog website uses the [Hugo](https://gohugo.io/) framework, with [Kiera](https://themes.gohugo.io/hugo-kiera/) theme.
I'm hosting the website using [Netlify](https://www.netlify.com/).

## Usage

* I can add new blog posts with `nvim content/post/$(date "+%Y-%m-%d")_TITLE.md`.
* If I use images I need to add them into the `static/` folder, I'm using the naming convention `$(date "+%Y-%m-%d")_IMAGE_TITLE.md` so that they are organized a bit.
* To test out the blog locally I just need to run `hugo server -D` and view the WIP at localhost:1313
* I can use `ngrok http 1313` to get a URL to share with people before I post an article.
* To actually publish a post I just need to make a commit and push it to Github, netlify will take care of the build and deployment.
