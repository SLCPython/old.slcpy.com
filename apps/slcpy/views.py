#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Viewing for SLCPy.com
AUTHOR: Dylan Gregersen
DATE: Thu Sep 25 12:56:23 2014
"""
# ########################################################################### #

from __future__ import print_function, division, unicode_literals
import os
from django.conf import settings
from django.shortcuts import render,render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from meetup.api import add_base_view_items

# ########################################################################### #

def home_view_no_next_event (request):
    """ View home without next event """
    context = RequestContext(request)    
    context_dict = dict()        
    add_base_view_items(context_dict)
    return render_to_response("slcpy/index.html",context_dict,context)
