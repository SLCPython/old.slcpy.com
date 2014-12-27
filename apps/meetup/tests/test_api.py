#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: For testing meetup api functions
AUTHOR: Dylan Gregersen
DATE: Sun Sep 28 18:25:15 2014
"""
# ########################################################################### #

# import modules

from __future__ import print_function, division, unicode_literals
from django.test import TestCase
from meetup.api import from_meetup_timestamp,to_meetup_timestamp
import unittest

# ########################################################################### #

class TestMeetupConversions (TestCase):
    
    def setUp(self):
        pass 
        
    def test_parse_meetup_time ():
        meetup_time = 1411338964000.0        
        sol = datetime.datetime(2014,9,21,16,36,4,tzinfo=pytz.timezone("US/Mountain"))
        # pass in tz as string
        tzinfo = "US/Mountain"
        ans = from_meetup_timestamp(meetup_time,tzinfo)
        assert sol == ans 

    def test_parse_meetup_time_tzinfo ():
        meetup_time = 1411338964000.0        
        sol = datetime.datetime(2014,9,21,16,36,4,tzinfo=pytz.timezone("US/Mountain"))    
        # pass in timezone as object
        tzinfo = pytz.timezone("US/Mountain")
        ans = from_meetup_timestamp(meetup_time,tzinfo)
        assert sol == ans 
            
    def test_to_meetup_timestamp ():        
        d = datetime.datetime(2014,9,21,16,36,4,tzinfo=pytz.timezone("US/Mountain"))
        sol = 1411338964000.0   
        ans = to_meetup_timestamp(d)
        assert sol == ans 
                
    def test_geo_stamp ():
        pass

