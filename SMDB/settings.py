# Django settings for SMDB project.
import os

def relative(*x): return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Pedro Gaspar', 'me@pedrogaspar.com'),
	('Miguel Tavares', 'mtavares.azrael@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'				# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'database/db.sqlite3'	# Or path to database file if using sqlite3.
DATABASE_USER = ''						# Not used with sqlite3.
DATABASE_PASSWORD = ''		   			# Not used with sqlite3.
DATABASE_HOST = ''						# Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''						# Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Lisbon'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = relative('media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e0vt=by1u#l)-hel#g+f87zqgz(n6x@c&=_@a!kd)-yk5uwy70'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
#	  'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'smdb.semantic_manager_middleware.SemanticMiddleware',
)

ROOT_URLCONF = 'SMDB.urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	relative('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.auth",
	"django.core.context_processors.media",
	"django.core.context_processors.request",
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'smdb',
	'django_rdf',
)

DEFAULT_GRAPH_URI = 'http://www.smdb.com/smdb.owl'
RDF_DATABASE_NAME = relative('database/rdf')

ITEMS_PER_PAGE = 10

AUTH_PROFILE_MODULE = 'smdb.UserProfile'
LOGIN_REDIRECT_URL = '/'