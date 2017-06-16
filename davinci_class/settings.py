from __future__ import absolute_import, unicode_literals
from os import path

####################
# DAVINCI SETTINGS #
####################

COURSE_CHOICES = (
    (1, 'Fall 2016'),
    (2, 'Spring 2017'),
)

CURRENT_COURSE = 2

RECORDING_PATH = None
RECORDING_HOLD_PATH = None
RECORDING_FILE_EXTENSION = 'm4a'

# API_TOKEN should be defined in local_settings
SLACK_API_TOKEN = None
SLACK_CHANNEL = '#python'

########
# BOTO #
########
# BOTO is the Amazon Web Services library
# These should be overridden in local_settings
AWS_ACCESS_KEY = None
AWS_SECRET_KEY = None

AWS_BUCKET = 'davinci-institute'


########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*', ]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

# Supported languages
LANGUAGES = (
    ('en', 'English'),
)

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644  # linux permissions -- 644 = owner read/write, others read

#############
# DATABASES #
#############

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.',
        # DB name or path to database file if using sqlite3.
        'NAME': '',
        # Not used with sqlite3.
        'USER': '',
        # Not used with sqlite3.
        'PASSWORD': '',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = path.dirname(path.abspath(__file__))  # __file__ is the absolute path to the current file
PROJECT_APP = path.basename(PROJECT_APP_PATH)  # dynamically name project based on folder
PROJECT_ROOT = BASE_DIR = path.dirname(PROJECT_APP_PATH)  # same as BASE_DIR in Django 1.11

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

# URL prefix for static files.
# Example: 'http://media.lawrence.com/static/'
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'
STATIC_ROOT = path.join(PROJECT_ROOT, 'local_static')

STATICFILES_DIRS = [
    path.join(BASE_DIR, 'static'),
    path.join(BASE_DIR, 'recordings', 'static'),
]

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/'
MEDIA_URL = STATIC_URL + 'media/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/media/'
MEDIA_ROOT = path.join(PROJECT_ROOT, *MEDIA_URL.strip('/').split('/'))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = '%s.urls' % PROJECT_APP

TEMPLATES = [
    # Zinnia
    {
        'DIRS': [
            path.join(PROJECT_ROOT, 'templates'),
            path.join(PROJECT_ROOT, 'recordings', 'templates'),
        ],
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'zinnia.context_processors.version',  # Optional
            ]
        }
    }

]

################
# APPLICATIONS #
################


INSTALLED_APPS = (
    # admin
    # 'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',
    # 'admin_tools_zinnia',
    'django.contrib.admin',

    # standard
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'django_comments',
    'mptt',
    'tagging',
    'zinnia',

    'recordings',
    'taggit',

    # dev
    'django_extensions',
    # 'debug_toolbar',

)
# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Uncomment if using internationalisation or localisation
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

##########
# ZINNIA #
##########

ZINNIA_MARKUP_LANGUAGE = 'markdown'
ZINNIA_MARKDOWN_EXTENSIONS = ['markdown.extensions.fenced_code', ]

##################
# Django Tagging #
##################

FORCE_LOWERCASE_TAGS = True

###########
# Logging #
###########

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format':
                '%(levelname)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'file_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': path.abspath(path.join(BASE_DIR, '../project.log')),
        },
        #        'rotating_file': {
        #            'level': 'DEBUG',
        #            'formatter': 'verbose',
        #            'filename':   MY_LOG_FILENAME, # full path works
        #            'class': 'logging.handlers.TimedRotatingFileHandler',
        #            'when': 'midnight',
        #            'interval': 7,
        #            'backupCount': 52,
        #        },
    },
    'loggers': {
        '': {
            'handlers': ['file_log', ],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', ],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backend': {
            'handlers': ['file_log', ],
            'propagate': True,
            'level': 'INFO',
        },
    },
}

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing 'from .local_settings import *', we use exec so that
# local_settings has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

f = path.join(PROJECT_APP_PATH, 'local_settings.py')
if path.exists(f):
    import sys
    import imp

    module_name = '%s.local_settings' % PROJECT_APP
    module = imp.new_module(module_name)
    module.__file__ = f
    sys.modules[module_name] = module
    exec (open(f, 'rb').read())
