#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

DEBUG = True

AUTHOR = u'Aaron Schif'
SITENAME = u'Swing & Salsa'
SITEURL = ''

THEME = "ballroom_theme"
WEBASSETS = True

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

PLUGIN_PATHS = [
    "../plugins"
]

PLUGINS = [
    'assets',
    'pelican_youtube',
]

SOCIAL = [
    {
        'name': "Facebook",
        'url': "https://www.facebook.com/groups/5882359073/",
        'img': "facebook.png"
    },
    {
        'name': "Email",
        'url': "mailto:ballroom-l@listserv.ksu.edu",
        'img': "email.png"
    },
    {
        'name': "YouTube",
        'url': "http://www.youtube.com/ksuswingsalsa",
        'img': "youtube.png"
    }
]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = False

PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}/index.html"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
