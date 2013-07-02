# Django settings for trueque project.
import os
RUTA_PROYECTO = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Gabriel Ruiz', 'gabriel.ruiz@skyvortex.cl'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'trueque',                      # Or path to database file if using sqlite3.
        'USER': 'admin',                      # Not used with sqlite3.
        'PASSWORD': 'kenolamasca2veces',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Santiago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 3

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DATE_FORMAT = "d M Y"

ugettext = lambda s: s
LANGUAGES = (
    ('es', ugettext('Spanish')),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(RUTA_PROYECTO, 'cargas')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(RUTA_PROYECTO, 'plantillas/static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'abkcjr)9eb6p25(a%y@469*=$@e5to91l3fd!^d$jx_(1u$%e+'

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
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    )

ROOT_URLCONF = 'trueque.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'trueque.wsgi.application'

TEMPLATE_DIRS = (
	os.path.join(RUTA_PROYECTO, 'plantillas/static')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',+
    'usuarios',
    'products',
    'main',
    'albums',
    'invitations',
    'messages',
    'notifications',
    'statistics',
    'transactions',
    'pagination',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#Django Social Auth Params
TWITTER_CONSUMER_KEY         = 'IVNcmsb91vVGpBOaYSeQqg'
TWITTER_CONSUMER_SECRET      = 'fcsmCpQV1wCcXpHjOZPuXMNX5mQC921hIb5qtLQwY'
FACEBOOK_APP_ID              = '172307212944741'
FACEBOOK_API_SECRET          = '1887a57c1a12becb8c1b1cc8483b2fe1'


#Email Params
EMAIL_HOST = 'smtp.google.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mail.trueque@gmail.com'
EMAIL_HOST_PASSWORD = 'kenolamasca2veces'
EMAIL_USE_TLS = True

WEB_URL = "http://localhost:8000"
#WEB_URL = "http://pruebas.trueque.in"

AUTH_USER_MODEL = 'usuarios.Usuario'
LOGIN_URL =  "/accounts/login"
LOGIN_REDIRECT_URL = "/"
AVATAR_STORAGE_DIR = 'media/avatars'

#Social Auth Params
TWITTER_CONSUMER_KEY         = 'IVNcmsb91vVGpBOaYSeQqg'
TWITTER_CONSUMER_SECRET      = 'fcsmCpQV1wCcXpHjOZPuXMNX5mQC921hIb5qtLQwY'
FACEBOOK_APP_ID              = '172307212944741'
FACEBOOK_API_SECRET          = '1887a57c1a12becb8c1b1cc8483b2fe1'



#================ AllAuth data ======================

ACCOUNT_ADAPTER ="allauth.account.adapter.DefaultAccountAdapter"

#Specifies the login method to use - whether the user logs in by entering his username, e-mail address, or either one of both.
ACCOUNT_AUTHENTICATION_METHOD ="email"

#The URL to redirect to after a successful e-mail confirmation, in case no user is logged in.
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL =LOGIN_URL

#The URL to redirect to after a successful e-mail confirmation, in case of an authenticated user. Set to None to use settings.LOGIN_REDIRECT_URL.
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL =None
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =3
ACCOUNT_EMAIL_REQUIRED =True

#ACCOUNT_EMAIL_VERIFICATION (="mandatory" | "optional" | "none")
ACCOUNT_EMAIL_VERIFICATION ="mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX ="[Trueque.in]"
ACCOUNT_LOGOUT_ON_GET =False
ACCOUNT_LOGOUT_REDIRECT_URL ="/"

#A string pointing to a custom form class (e.g. 'myapp.forms.SignupForm') that is used during signup to ask the user for additional input 
ACCOUNT_SIGNUP_FORM_CLASS =None
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION =True
ACCOUNT_UNIQUE_EMAIL =True
ACCOUNT_USER_MODEL_USERNAME_FIELD ="username"
ACCOUNT_USER_MODEL_EMAIL_FIELD ="email"

#A callable (or string of the form 'some.module.callable_name') that takes a user as its only argument and returns the display name of the user. The default implementation returns user.username.
#ACCOUNT_USER_DISPLAY =Usuario.get_full_name()
ACCOUNT_USERNAME_MIN_LENGTH =4
ACCOUNT_USERNAME_BLACKLIST =[]
ACCOUNT_USERNAME_REQUIRED = False

#render_value parameter as passed to PasswordInput fields.
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE =False
ACCOUNT_PASSWORD_MIN_LENGTH =6

#Specifies the adapter class to use, allowing you to alter certain default behaviour.
SOCIALACCOUNT_ADAPTER ="allauth.socialaccount.adapter.DefaultSocialAccountAdapter"

#Request e-mail address from 3rd party account provider? E.g. using OpenID AX, or the Facebook "email" permission.
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED

#Attempt to bypass the signup form by using fields (e.g. username, email) retrieved from the social account provider. If a conflict arises due to a duplicate e-mail address the signup form will still kick in.
SOCIALACCOUNT_AUTO_SIGNUP =True

#Enable support for django-avatar. When enabled, the profile image of the user is copied locally into django-avatar at signup.
SOCIALACCOUNT_AVATAR_SUPPORT = 'avatar' in INSTALLED_APPS

#The user is required to hand over an e-mail address when signing up using a social account.
SOCIALACCOUNT_EMAIL_REQUIRED =ACCOUNT_EMAIL_REQUIRED

#As ACCOUNT_EMAIL_VERIFICATION, but for social accounts.
SOCIALACCOUNT_EMAIL_VERIFICATION ="none"

#Dictionary containing provider specific settings.
SOCIALACCOUNT_PROVIDERS = dict



#======= Facebook Auth Settings =========
SOCIALACCOUNT_PROVIDERS = \
    { 'facebook':
        { 'SCOPE': ['email'],
          'AUTH_PARAMS': { 'auth_type': 'https' },
          'METHOD': 'oauth2' ,
          'LOCALE_FUNC': lambda request: 'es_LA'} }

