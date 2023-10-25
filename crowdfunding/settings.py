"""
Django settings for crowdfunding project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2g01&1zrujcc(pnu*!k9i@!9rtp(ztz6p+^&6%1@)72)n!2im('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication.apps.AuthenticationConfig',
    'user.apps.UserConfig',
    'mainproject.apps.MainprojectConfig',
    'homepage.apps.HomepageConfig',

    'rest_framework',
    'social_django',
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
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <-- Here

]

ROOT_URLCONF = 'crowdfunding.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect',  # <-- Here

            ],
        },
    },
]

WSGI_APPLICATION = 'crowdfunding.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'crowd_funding',
        'USER': 'postgres',
        'PASSWORD': '111',
        'PORT': 5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATIC_URL = 'static/'
# STATICFILES_DIRS=['static']
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'crowdfunding/static')
]

#Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


AUTH_USER_MODEL = 'user.User'
SOCIAL_AUTH_USER_MODEL = 'user.User'
# AUTHENTICATION_BACKENDS = (
#     'social_core.backends.facebook.FacebookOAuth2',
#     'social_core.backends.twitter.TwitterOAuth',
#     'social_core.backends.github.GithubOAuth2',
#
#     'django.contrib.auth.backends.ModelBackend',
# )
## social setup
# Now set the default values for the LOGIN_URL, LOGOUT_URL ,LOGIN_REDIRECT_URL
# LOGIN_REDIRECT_URL : used to redirect the user after authenticating from Django Login and Social Auth.

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'





# SOCIAL_AUTH_FACEBOOK_SCOPE = [
#     'email',
# ]
#
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
#     'email',
# ]
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
#     'fields': 'first_name,last_name,email,picture'
# }

#Social keys

# SOCIAL_AUTH_FACEBOOK_KEY = SOCIAL_AUTH_FACEBOOK_KEY    # App ID
# SOCIAL_AUTH_FACEBOOK_SECRET = SOCIAL_AUTH_FACEBOOK_SECRET  # App Secret
SOCIAL_AUTH_FACEBOOK_KEY = '1707430803095433'
SOCIAL_AUTH_FACEBOOK_SECRET = '30c94fdfad6190e82a8a1791dad1690f'

#
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY  # App ID
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET  # App Secret
#


SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


#email verication:
# settings.py
# Email verifications
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# # coming from the secrets file
# EMAIL_HOST_USER = EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'enasmetwally99@gmail.com'
EMAIL_HOST_PASSWORD = 'ltfr rtiy xfpe axau'

#ltfr rtiy xfpe axau

