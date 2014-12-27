#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Methods and functions to assist-viewing/view content
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
from meetup.api import meetup_client, add_etherpad_urls 
from urllib2 import HTTPError

SLCPY_MEETUP_URL = settings.SLCPY_MEETUP_URL

# ########################################################################### #

VIEW_TIMEZONE = "" #"America/Denver"
                        
# ########################################################################### #

def add_base_view_items (context_dict):
    """ Add some keys desired for the base view """
    context_dict['slcpy_meetup_url'] = SLCPY_MEETUP_URL
    context_dict['slcpy_meetup_url_join'] = os.path.join(SLCPY_MEETUP_URL,"join")
    return context_dict
    
def cache_response (func):
    """ Cache and return the response from function """
    def view_func (request,re_cache=False):
        # TODO: implement caching, if cached, else
        return func(request)
    view_func.__doc__ = func.__doc__
    return view_func
    
@cache_response
def home_view (request):
    """ Home with next event """
    context = RequestContext(request)    
    context_dict = dict()        
    add_base_view_items(context_dict)
    try:
        next_event = meetup_client.get_next_group_event(tzinfo=VIEW_TIMEZONE) 
        context_dict['next_event'] = next_event
    except HTTPError:
        pass
    return render_to_response("meetup/index.html",context_dict,context)

@cache_response
def view_upcoming_past_events (request):
    """ View all upcoming and past events """
    context = RequestContext(request)    
    context_dict = dict()        
    add_base_view_items(context_dict)
    events = meetup_client.get_upcoming_and_past_group_events(tzinfo=VIEW_TIMEZONE)     
    for i in range(len(events)):
        add_etherpad_urls(events[i])
    context_dict['events'] = events
    return render_to_response("meetup/events.html",context_dict,context)
    
    
pass 
# ########################################################################### #

# view meetup.com in a frame

# TODO: not working yet    
    
missing_meetup_template = """  

<h2> ERROR : Unable to get Meetup.com SLCPython home </h2>

<p>
    Try to use this <a href="{}">link to our Meetup.com</a>
</p>        
        """

# {{ meetup_home|safe }}
def strip_meetup_response (response,context_dict):
    """ Take response from meetup and overwrite """

    # ======================= header from meetup page
    i = response.find("<head>")
    j = response.find("</head>")
    key = 'meetup_home_head'
    if i >= 0 and j >= 0:
        context_dict[key] = response[i+6:j]
    else:
        context_dict[key] = "\n"
        
    # ======================= body from meetup page
    i = response.find("<body ")
    j = response.find("</body>")
    key = 'meetup_home_body'
    if i >= 0 and j >= 0:
        fmt = '<body id="meetupBody" class="humble slcpy-meetup-home" >\n {} \n</body>'
        body = fmt.format(response[i+6:j])
        context_dict[key] = body
    else:
        url = context_dict['request-url']       
        context_dict[key] = missing_meetup_template.format(url)
    # ======================= return context 
    return context_dict

def meetup_home_view (request):
    """ Wrap the SLCPython Meetup Home"""
    context = RequestContext(request)    
    url = SLCPY_MEETUP_URL
    user_agent = request.META['HTTP_USER_AGENT']
    headers = {'User-Agent':user_agent}
    context_dict = {'request-url':url}
    try:
        req = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(req).read()
    except urllib2.URLError as e:
        raise e 
    context_dict["meetup_home"] = response
#     context_dict = strip_meetup_response(response,context_dict)   
    return render_to_response("meetup/meetup_home.html",context_dict,context)
