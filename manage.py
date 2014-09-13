#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    # decide which settings to use
    base_dir = os.path.dirname(__file__)
    local_settings_module = "slcpy/settings/local_settings.py")    
    if os.path.isfile(os.path.join(base_dir,"apps",local_settings_module)):
        django_settings_module = local_settings_module
    else:
        django_settings_module = "slcpy.settings.local"

    # set the local settins
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",django_settings_module)

    # execute from command line
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
