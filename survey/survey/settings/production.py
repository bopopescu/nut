from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'survey',                      # Or path to database file if using sqlite3.
        'USER': 'guoku',                      # Not used with sqlite3.
        'PASSWORD': 'guoku1@#',                  # Not used with sqlite3.
        'HOST': '10.0.2.90',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

__author__ = 'edison7500'
