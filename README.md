slcpy.com
=========

Official Repo of SLCPython's website

[twitter](https://twitter.com/slcpy)
[meetup](www.meetup.com/Salt-Lake-City-Python-Web-Developers/)

## Local Dev Set up

Install virtualenv & virtualenvwrapper

Activate virtualenvwrapper

`mkvirtualenv slcpy`

Add localsettings to virtualenv:

In `~/.virtualenvs/slcpy/bin/postactivate` add this line →`export DJANGO_SETTINGS_MODULE=slcpy.settings.local`

Add apps to your virtualenv:

    add2virtualenv `pwd`/apps # note the backticks

Deactivate and reactivate virtualenv in the slcpy folder:

`deactivate && workonslcpy`

## Production deployment

## Contributing
