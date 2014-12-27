#!/usr/bin/env python
import os
import sys
import django

if __name__ == "__main__":

    # decide which settings to use
    base_dir = os.path.dirname(__file__)
    local_settings_module = ["slcpy","settings","local_settings"]
    
    filepath = os.path.join(base_dir,"apps","/".join(local_settings_module)+".py")
    if os.path.isfile(filepath):
        django_settings_module = ".".join(local_settings_module)
    else:
        django_settings_module = "slcpy.settings.local"
    
    # set the local settins
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",django_settings_module)
    
    # execute from command line
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
