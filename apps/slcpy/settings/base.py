"""
Django settings for slcpy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(\
    os.path.abspath(\
        os.path.join(os.path.dirname(__file__),"..","..")
        )
    )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n>!k#o/{JLtum(mE2MO^M^SX=3T@{epi=sbro7*9]o(k<oOEtH'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

# template handling 
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,"apps", "slcpy", "templates"),
    os.path.join(BASE_DIR,"apps", "meetup", "templates"),    
)

TEMPLATE_PATH = ":".join(TEMPLATE_DIRS)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

ALLOWED_HOSTS = [
    'slcpy.com',
    'slcpy.metacogni.tv.',
]

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'slcpy', # metapp for settings
    'meetup',
)

THIRD_PARTY_APPS = (
    'meetup',
    'taggit',
    'tastypie',
    'south',
    'haystack',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'slcpy.urls'

WSGI_APPLICATION = 'slcpy.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#AUTH_USER_MODEL = "profiles.SLCPyUser"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, "globalstatic")
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, "media"))

# Haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.normpath(os.path.join(BASE_DIR, "whoosh_index")),
    }
}

# Our site can handle this
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# ########################################################################### #


GITHUB_URL = "https://github.com/SLCPython"

# Meetup

# This is hard coded so that we don't have to rely on the meetup_client from your
# MEETUP_API_KEY
SLCPY_MEETUP_URL = "http://www.meetup.com/Salt-Lake-City-Python-Web-Developers/"

# MEETUP_API_KEY **Security Warning:** Keep personal Meetup api key secret.
# Read `Meetup documentation <https://secure.meetup.com/meetup_api/key/>`_.
# create a file "slcpy.com/apps/slcpy/settings/local_settings.py" 
# which won't be tracked by git and add the lines
# from local import *
# MEETUP_API_KEY = "abc123"
MEETUP_API_KEY = ""

# (optional) This is the default group id to get information from  
MEETUP_GROUP_ID = 12004972

try:
    from local_settings import *
except:
    pass

