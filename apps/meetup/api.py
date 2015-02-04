#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Tools to access the Meetup.com API
AUTHOR: dylangregersen
DATE: Mon Sep 15 00:12:21 2014
"""
# ########################################################################### #

# import modules 

from __future__ import print_function, division, unicode_literals
import os
import time
import datetime
import pytz
import arrow
from django.conf import settings
from meetup.models import EtherpadNote
from urllib import urlencode
from urllib2 import urlopen
try:
    import json
except ImportError:
    import simplejson as json

MEETUP_API_KEY =  settings.MEETUP_API_KEY
MEETUP_GROUP_ID =  getattr(settings,'MEETUP_GROUP_ID',"")

# ########################################################################### #

def venue_google_search_url (venue_data):
    """ 
    
    Parameters
    venue_data : dict
    
    Returns
    url : string
    
    """
    keywords = ("{name}","{city}","{state}","{country}","{address_1}")
    search = "+".join(keywords)
    search = search.format(**venue_data).replace("/","_").replace(" ","+")
    url = "https://www.google.com/maps/place/"+search
    return url

def from_meetup_timestamp (t,tzinfo=""):
    """ Take time stamp from Meetup, convert to datetime 
    assumes utc if not tzinfo is given

    Parameters
    ----------
    t : integer
        time in milliseconds
    tzinfo : string or pytz.timezone object
    
    """
    # convert to structured time
    struct_time = time.gmtime(int(t) / 1000.0)    
    # get datetime object
    keys = ['year','month','day','hour','minute','second']
    kws = {k:struct_time[i] for i,k in enumerate(keys)}
    kws['tzinfo'] = pytz.utc
    dt = arrow.Arrow(**kws)
        
    # apply timezone info if needed
    if isinstance(tzinfo,datetime.tzinfo):
        return dt.to(tzinfo)
    elif len(tzinfo):
        return dt.to(pytz.timezone(tzinfo))
    else:
        return dt

def to_meetup_timestamp (ts):
    """ Convert to meetup's time stamp """
    tzinfo = str(ts.tzinfo)
    t = time.mktime(d.timetuple())/1000.0
    return t,tzinfo

def enrich_event_data (event_data,tzinfo=""):
    """ Add fields to meetup event_data
    
    Parameters
    event_data : dict
    
    Returns
    event_data : dict
        Added fields, Note that this modifies the input event_data by reference
        as well
    
    """
    if event_data['status'] == "upcoming":
        event_data['css_style'] = "panel-success"
    elif event_data['status'] == "past":
        event_data['css_style'] = "panel-info"
    else:
        event_data['css_style'] = "panel-default"

    event_data['timestamp'] = from_meetup_timestamp(event_data['time'],tzinfo)
    event_data['venue']['google_url'] = venue_google_search_url(event_data['venue'])
    return event_data

class MeetupClient(object):
    """ MeetupClient """
    
    api_meetup_url = "https://api.meetup.com"
    
    def __init__(self, api_key):
        """ Find your api_key from https://secure.meetup.com/meetup_api/key/"""
        self.api_key = api_key    
                
    def signed_request_url (self,meetup_method,params=None,request_hash=None):
        """ To GET data from api.meetup.com 
        
        """                
        # get the parameters 
        params = params.copy() if params is not None else {}
        params['signed'] = True
        
        response = self.http_response(meetup_method,params,method='GET')
        signed_url = response['signed_url']
        return signed_url
    
    def http_response (self, meetup_method, params=None, method='GET'):
        """ For request http response from meetup
        
        Parameters
        meetup_method : string
            see http://www.meetup.com/meetup_api/docs/
        params : dict or None
            parameters passed to the request                    
        method : string  
            'GET' or 'POST'
        
        Returns
        response : dict
        
        """
        # TODO: rename http_response to http_response        
        
        # get the parameters 
        params = params.copy() if params is not None else {}
        params['key'] = self.api_key
        params['page'] = 1000
                
        # the specific meetup method
        # see http://www.meetup.com/meetup_api/docs/
        if meetup_method.startswith("/"):
            meetup_method = meetup_method[1:]        
        url = os.path.join(self.api_meetup_url,meetup_method)
        
        # get response
        if method == 'GET':
            return self._get(url, params)
        elif method == 'POST':
            return self._post(url, params)
    
    def _get(self, url, params):
        url = "{}?{}".format(url, urlencode(params))
        content = urlopen(url).read()
        content = unicode(content, 'utf-8', 'ignore')
        return json.loads(content)
        
    def _post(self, url, params):
        content = urlopen(url, urlencode(params)).read()
        content = unicode(content, 'utf-8', 'ignore')
        return json.load(content)
    
    def get_group_events (self,group_id=None):
        if group_id is None:
            group_id = settings.MEETUP_GROUP_ID
        return self.http_response("/2/events",params=dict(group_id=group_id))['results']
      
    def get_next_group_event (self,group_id=MEETUP_GROUP_ID,tzinfo="utc"):
        """ Recover the next upcoming event for a group

        default group is from ``django.conf.settings.MEETUP_GROUP_ID``. If None then
        you will have to give the group explicitly when calling this function

        Parameters
        ----------
        group_id : int or str 
            meetup group_id

        Returns
        -------
        next : event_data or None

        """
        if isinstance(group_id,basestring):
            group_id = int(group_id)
        params = dict(group_id=group_id,status="upcoming")
        events = self.http_response("/2/events",params=params)['results']
        if not len(events):
            return        
        next_event = events[0]
        return enrich_event_data(next_event,tzinfo)

    def get_upcoming_and_past_group_events (self,group_id=MEETUP_GROUP_ID,tzinfo="utc"):
        if isinstance(group_id,basestring):
            group_id = int(group_id)
        params = dict(group_id=group_id,status="upcoming,past")
        events = self.http_response("/2/events",params=params)['results']
        for i in range(len(events)):
            enrich_event_data(events[i],tzinfo)
        return list(reversed(events))
            
    def get_group_info (self,group_id=None):
        if group_id is None:
            group_id = settings.MEETUP_GROUP_ID
        return self.http_response("/2/groups",params=dict(group_id=group_id))['results']            
                          
meetup_client = MeetupClient(MEETUP_API_KEY)

# ########################################################################### #

# For tracking etherpad 

def find_etherpad_urls (meetup_client,event_id):
    """ Find all etherpad urls for a given meetup event by searching the comments
    
    Parameters
    meetup_client : MeetupClient
    event_id : int or string 
        The meetup event_id 
    
    """
    # regular expression to match etherpad urls
    regex = "(http(s)?://etherpad.mozilla.org/[a-z,A-Z,0-9,_,-,$]*)"        
    if isinstance(event_id,basestring):
        event_id = int(event_id)
    # get all event comments
    params = dict(event_id=event_id)
    comments = meetup_client.http_response("/2/event_comments",params=params)['results']    
    # search each comment for etherpad urls
    etherpad_urls = []
    for comment in comments:
        s = re.search(regex,comment['comment'])
        if s is not None:
            etherpad_urls.append(s.groups()[0])            
    return etherpad_urls

def add_etherpad_urls (event_data):
    """ Add item etherpad_urls"""
    event_id = event_data['id']
    # query our database or
    #etherpad_urls = find_etherpad_urls(event_id)
    #event_data['etherpad_urls'] = etherpad_urls
    return event_data



