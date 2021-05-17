"""
Django settings for linkSite project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=e-10$2n%#r(hhzdqkf)xr1oi&#!=+b!6=--g)z#d5ct9eih!3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_registration',
    'links.apps.LinksConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linkSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'linkSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "base"

ACCOUNT_ACTIVATION_DAYS = 7

#AUTH_USER_MODEL = 'links.User'


def requests_filter(record):
    if type(record.args) is tuple:
        if any('GET' in args for args in record.args) or any('POST' in args for args in record.args):
            return False
    return True


def request_filter2(record):
    if type(record.args) is tuple:
        if any('GET' in args for args in record.args) or any('POST' in args for args in record.args):
            return True
    return False


LOGGING = {
    'version': 1,
    'filters': {
        'requests_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': requests_filter
        },
        'requests_filter2': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': request_filter2
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'request_file'],
            'level': 'INFO'
        },

    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'filters': ['requests_filter'],
            'class': 'logging.FileHandler',
            'filename': './logs/myLinks.log',
            'formatter': 'simple',
        },

        'request_file': {
            'level': 'INFO',
            'filters':['requests_filter2'],
            'class': 'logging.FileHandler',
            'filename': './logs/myLinks_http.log',
            'formatter': 'simple',
        }
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(message)s'
        }
    }
}

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USER_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@safelinks.app'
