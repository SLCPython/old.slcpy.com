import os
from .base import *

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/slcpy-messages'
DEFAULT_FROM_EMAIL = 'faris@theluckybead.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', '..', 'slcpy.db'),
    }
}

WSGI_APPLICATION = 'slcpy.wsgi.dev.application'

