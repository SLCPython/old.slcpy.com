# encoding: utf-8
import os
import re

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.request import QueryDict
from django.core.context_processors import csrf

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

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
    return render_to_response("slcpy/index.html",context_dict,context)
