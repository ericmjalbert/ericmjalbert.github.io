#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Eric Jalbert"
SITENAME = "Eric M. Jalbert"
SITEURL = "//ericmjalbert.netlify.com"
SITEURL = "//localhost:8000"

PATH = "content"

TIMEZONE = "America/Toronto"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
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

DEFAULT_PAGINATION = 10


##### Theme settings
THEME = "./pelican-purple"

SIDEBAR_DIGEST = (
    "Working at the intersection of Engineering, Data Analytics, and Statistics."
)

STATIC_PATHS = ["img"]
FAVICON = "img/favicon.ico"

DISPLAY_PAGES_ON_MENU = True

MENUITEMS = (
    ("Blog", SITEURL),
    ("About Me", SITEURL + "/about-me"),
    ("Projects", SITEURL + "/tag/project"),
    ("Tags", SITEURL + "/tags"),
)
#####

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
