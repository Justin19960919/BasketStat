"""
Django settings for basketstat project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=$qf@waq$fbr6k5q&5j$@a3j64@ai#tx-&6g+nd0)!*(8a7d5='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    # '4f98a9d50ed6.ngrok.io', # for ngrok connections
]


# Application definition

INSTALLED_APPS = [
    'my_app.apps.MyAppConfig',
    'player.apps.PlayerConfig',
    'game.apps.GameConfig',
    'home.apps.HomeConfig',
    'posts.apps.PostsConfig',
    'usrs.apps.UsrsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',

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

ROOT_URLCONF = 'basketstat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'basketstat.wsgi.application'


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# tells Django to append static to the base url (in our case localhost:8000) when searching for static files // in development
# if we wish, we can create one for each app
STATIC_URL = '/static/'

# loading static files (documentation)
# https://learndjango.com/tutorials/django-static-files
# https://www.mattlayman.com/understand-django/serving-static-files/
'''
This means that static files will be stored in the location 
http://127.0.0.1:8000/static/ or http://localhost:8000/static/. 
In order to notify Django of our new top-level static folder, 
we must add a configuration for STATICFILES_DIRS telling Django to also look within a static folder.
'''
# STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),) 
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# for deployment, check out the upper two links
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Dir to store uploaded files
# Set media root (Directory that uploaded files will be saved)
# Pu the profile_pics folder in the media folder
# Not saved in database for performance
# os.path.join will ensure the path is joined correctly whatever os
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    # upload dir
MEDIA_URL = '/media/'   # public url of the directory




# tell django we want our crispy forms to use the bootstrap4 css framework
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# change login redirect url
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

### EMAILS
## set up for sending emails for password reset
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# configure to dotenv later
# load from private environment
# EMAIL_HOST_USER = 'wadesuperstar@gmail.com'
# EMAIL_HOST_PASSWORD = 'aafdadfasdadsfcasdfad'

EMAIL_HOST_USER = os.getenv('EMAIL')
EMAIL_HOST_PASSWORD = os.getenv('PWD')












