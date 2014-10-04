#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE:
AUTHOR: Dylan Gregersen
DATE: Thu Sep 25 13:18:21 2014
"""
# ########################################################################### #
from django.db import models

# Create your models here.

class EtherpadNote (models.Model):
    
    # event_id
    # etherpad_id
    # text
    etherpad_id = models.IntegerField(unique=True)   
    etherpad_url = models.URLField() 
    event_id = models.IntegerField() # Forgien Field
    event_name = models.CharField(max_length=255)    
    text = models.TextField(blank=True) 
    
    def __unicode__ (self):
        return self.event_name

    def short_text (self,length=50):
        desc = self.text[:length]
        if len(desc) == length:
            desc = desc[:-3] + "..."
        return desc    
    