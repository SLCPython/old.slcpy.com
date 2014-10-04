#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: For allowing getting information from Etherpad
AUTHOR: Dylan Gregersen
DATE: Thu Sep 25 14:43:13 2014
"""
# ########################################################################### #

# import modules 

from __future__ import print_function, division, unicode_literals
import os 
import sys 
import re 
import time
import urllib2

# ########################################################################### #

url = "https://etherpad.mozilla.org/MEt0i42FxU"
def get_mopad_html (url):
    """ GET request to etherpad.mozilla.org for the html of mopad """
    s = re.search("^http.*mozilla\.org/(.*)",url)
    if s is not None:
        pad_name = s.groups()[0]
    else:
        raise ValueError("")
    request_url = "https://etherpad.mozilla.org/ep/pad/export/{}/latest?format=html".format(pad_name)
    text = urllib2.urlopen(request_url).read()
    return text 
