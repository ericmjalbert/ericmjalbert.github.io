#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Eric Jalbert"
SITENAME = "Eric M. Jalbert"
SITEURL = "http://ericmjalbert.github.io"

PATH = "content"

TIMEZONE = "America/Toronto"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "http://getpelican.com/"),
    ("Python.org", "http://python.org/"),
    ("Jinja2", "http://jinja.pocoo.org/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (("You can add links in your config file", "#"), ("Another social link", "#"))

DEFAULT_PAGINATION = 10


##### Theme settings
THEME = "./pelican-purple"

SIDEBAR_DIGEST = (
    "Working at the intersection of Engineering, Data Analytics, and Statistics."
)

FAVICON = "https://favicon.io/favicon-generator/?t=Ej&ff=Open+Sans&fs=100&fc=%23FFFFFF&b=rounded&bc=RGB%28103%2C84%2C+163%29"

DISPLAY_PAGES_ON_MENU = True

TWITTER_USERNAME = "twitter-user-name"

MENUITEMS = (("Blog", SITEURL),("About Me", SITEURL+"about-me") )
#SITEURL = "http://localhost:8000"
#####

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
