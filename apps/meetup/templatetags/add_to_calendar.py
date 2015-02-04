#!/usr/bin/env python
"""
PURPOSE: Filters for Meetup related objects
AUTHOR: Dylan Gregersen
DATE: Thu Sep 25 12:56:23 2014
"""

# ########################################################################### #

from __future__ import print_function, division, unicode_literals
import os
from arrow.util import timedelta
from django.conf import settings
from django import template
from django.utils.http import urlquote_plus
from collections import OrderedDict


EVENT_DURATION = 1.5 # hours

register = template.Library()

@register.filter
def google_calendarize(event):
    """
    <a href="http://www.google.com/calendar/event?
    action=TEMPLATE
    &text=[event-title]
    &dates=[start-custom format='Ymd\\THi00\\Z']/[end-custom format='Ymd\\THi00\\Z']
    &ctz=America/New_York
    &details=[description]
    &location=[location]
    &trp=false
    &sprop=
    &sprop=name:"

    target="_blank" 
    rel="nofollow">Add to Google Calendar</a>


    https://developers.google.com/google-apps/calendar/v3/reference/events/insert

    """
    not_valid = not len(event)
    not_valid &= event['status'] != 'upcoming'
    if not_valid:
        return ""

    start = event['timestamp']
    end = start + timedelta(hours=EVENT_DURATION)    
    tfmt = '%Y%m%dT000000'
    tfmt = "YYYYmMd\\THimm\\Z"

    # parameters
    params = OrderedDict()
    params['action'] = 'TEMPLATE'
    params['title'] = urlquote_plus(event['name'])
    # params['dates'] = "{}/{}".format(start.format(tfmt),end.format(tfmt))
    params['ctz'] = start.tzinfo
    params['details'] = urlquote_plus(event['description'])
    if 'venue' in event:
        venue = event['venue']
        location = [venue.get(key,"") for key in ('name','city','address_1')]
        params['location'] = urlquote_plus(", ".join(location))
    params['trp'] = 'False'

    # properties
    sprop = OrderedDict()
    # sprop["name"] = "hello+world"
    # sprop['website'] = urlquote_plus(Site.objects.get_current().domain)

    # create link
    link = ["{}={}".format(k,params[k]) for k in params]
    for k in sprop:
        link.append("sprop={}:{}".format(k,sprop[k]))

    link = "http://www.google.com/calendar/event?"+"&".join(link)

    return link

google_calendarize.safe = True
