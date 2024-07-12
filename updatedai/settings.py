"""
Django settings for updatedai project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from decouple import config

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = [
    '43.207.81.2',                     
    'ec2-43-207-81-2.ap-northeast-1.compute.amazonaws.com',
    'localhost',                      
    '127.0.0.1',                      
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',            # Add this line back
    'duffel',
    'memberships',
    'payments',
    'django.contrib.contenttypes',    # Add this line back
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    "corsheaders",
    'authentication',
    'account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "updatedai.middleware.SecurityHeadersMiddleware",
    "updatedai.middleware.JWTAuthenticationMiddleware",
    "updatedai.middleware.SaveUserActivityMiddleware",
]

# AUTH_USER_MODEL =  

ROOT_URLCONF = 'updatedai.urls'

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

WSGI_APPLICATION = 'updatedai.wsgi.application'


JWT_AUTH = {
    'JWT_AUTH_COOKIE': 'JWT',     # the cookie will also be sent on WebSocket connections
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=200),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN' : False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': '_id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=200),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # ... other authentication classes
    ],
     'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    # ... other settings
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_WHITELIST = []


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

OPENAI_API_KEY = config('OPENAI_API_KEY')

Pinecone_API = config('Pinecone_API')
Pinecone_env = config('Pinecone_env')

PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION = config('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION')

E2B = config('E2B')

TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_SERVICE_SID = config('TWILIO_SERVICE_SID')

STABLE_DIFUSSION_API_KEY = config('STABLE_DIFUSSION_API_KEY')

# CONVEX
CONVEX_DEPLOYMENT = config('CONVEX_DEPLOYMENT')
CONVEX_URL = config('CONVEX_URL')

# SMS
MESSAGING_SERVICE_SID = config('MESSAGING_SERVICE_SID')

# Email
EMAIL_CONFIRM_EMIL_TEMPLATE_ID = config("EMAIL_CONFIRM_EMIL_TEMPLATE_ID")
EMAIL_REQUEST_RESET_PASSWORD_TEMPLATE_ID = config("EMAIL_REQUEST_RESET_PASSWORD_TEMPLATE_ID")
EMAIL_FROM = config("EMAIL_FROM")
EMAIL_FROM_NAME = config("EMAIL_FROM_NAME")

# Duffel
DUFFEL_ACCESS_TOKEN = config("DUFFEL_ACCESS_TOKEN")

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY")

STRIPE_SIGNING_KEY = config("STRIPE_SIGNING_KEY")

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')