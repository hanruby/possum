from os.path import abspath, basename, dirname, join, normpath, exists
import os
import random
import sys

########## PATH CONFIGURATION
# Absolute filesystem path to this Django project directory.
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
# Site name.
#SITE_NAME = basename(DJANGO_ROOT)
SITE_NAME = "possum"
# Absolute filesystem path to the top-level project folder.
SITE_ROOT = dirname(DJANGO_ROOT)
# Add all necessary filesystem paths to our system path so that we can use
# python import statements.
sys.path.append(SITE_ROOT)
sys.path.append(normpath(join(DJANGO_ROOT, SITE_NAME, 'base')))
# sys.path.append(normpath(join(DJANGO_ROOT, 'possum.libs')))
########## END PATH CONFIGURATION

########## Configuration de POSSUM
LONGUEUR_FACTURE = 35
LONGUEUR_IHM = 60
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/bills'
# tmp est en memoire (tmpfs)
PATH_TICKET = normpath(join(DJANGO_ROOT, SITE_NAME, 'tickets'))
# list of authorized permissions codename
PERMS = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']
########## END POSSUM CONFIGURATION

########## KEY CONFIGURATION
# Absolute filesystem path to the secret file which holds this project's
# SECRET_KEY. Will be auto-generated the first time this file is interpreted.
SECRET_FILE = normpath(join(DJANGO_ROOT, SITE_NAME, 'secret_key'))

# Try to load the SECRET_KEY from our SECRET_FILE. If that fails, then generate
# a random SECRET_KEY and save it into our SECRET_FILE for future loading. If
# everything fails, then just raise an exception.
def create_secret_key():
    secret_key_text = ""
    with open(abspath(SECRET_FILE), 'w') as f:
        secret_key_text = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])
        f.write(secret_key_text)
    return secret_key_text

try:
    if os.path.isfile(SECRET_FILE):
        secret_key_text = open(SECRET_FILE).read()
        if not secret_key_text :
            secret_key_text = create_secret_key()
    else:
        secret_key_text = create_secret_key()
    SECRET_KEY = secret_key_text 
except IOError as e :
        raise Exception('Cannot open file `%s` for writing. (%s)' % (SECRET_FILE, e))
########## END KEY CONFIGURATION


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/home/pos/memcached.sock',  # TODO normpath(join(DJANGO_ROOT ,'memcached.sock'))
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr-fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DEFAULT_FROM_EMAIL = "noreply@example.org"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = normpath(join(DJANGO_ROOT, SITE_NAME, 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(DJANGO_ROOT, SITE_NAME , 'static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i!fd_s1ms-#ogdsStSdgwb=@9%vyq&69!yd-mr9hco7h73+#5u'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'possum.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'possum.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(DJANGO_ROOT, SITE_NAME, 'templates')),
)

INSTALLED_APPS = (
    'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chartit',
    'possum.base',
    'django_extensions',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
