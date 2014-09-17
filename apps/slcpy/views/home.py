#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules

from __future__ import print_function, division, unicode_literals
import os
import re
import urllib2
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.request import QueryDict
from django.core.context_processors import csrf

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

# ########################################################################### #

from meetup.views import next_group_event

def is_user_logged_in (context):
    """ Check if a user is connected
    
    Parameters
    context :
    
    Returns
    user_info :   or None
        user information or None if no user is connected
    
    """
    return 

def main_view (request):
    """ SLCPython Home """
    # get web context
    context = RequestContext(request)    
    # check for SLCPython users
    user_info = is_user_logged_in(context)
    if user_info is not None:
        pass    
    context_dict = dict()    
    context_dict['next_event'] = next_group_event() 

    context_dict['next_venue'] = context_dict['next_event'].venue.get()
    return render_to_response("meetup/index.html",context_dict,context)

# ########################################################################### #

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
    url = "http://www.meetup.com/Salt-Lake-City-Python-Web-Developers/"
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
    