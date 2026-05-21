import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key-for-local')
DEBUG = True
# DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
# SECRET_KEY = "django-insecure-ui-7+=ba=9uica51g=d))qr&+z$xj(5+&no7fiuh*-5q^d%-@s"


ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'storages',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',

    'django_eventstream',

    'accounts',
    'chat'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
}

SIMPLE_JWT = {
    # "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "BLACKLIST_AFTER_ROTATION": True,
    "ROTATE_REFRESH_TOKENS": True,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

EVENTSTREAM_STORAGE_CLASS = 'django_eventstream.storage.DjangoStorage'
EVENTSTREAM_CHANNELMANAGER_CLASS = (
    "chat.utils.ChatChannelManager"
)

ROOT_URLCONF = "PrivateAi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "PrivateAi.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BROKER_URL = "redis://redis:6379/1"
CELERY_RESULT_BACKEND = "redis://redis:6379/2"

EVENTSTREAM_REDIS = {
    'host': 'redis',
    'port': 6379,
    'db': 0,
}

USER_STORAGE_LIMIT = 1 * 1024 * 1024 * 1024

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = os.environ.get('MINIO_ROOT_USER')
AWS_SECRET_ACCESS_KEY = os.environ.get('MINIO_ROOT_PASSWORD')
AWS_STORAGE_BUCKET_NAME = 'media'

AWS_S3_ENDPOINT_URL = 'http://minio_s3:9000'
AWS_S3_CUSTOM_DOMAIN = f'localhost:9000/{AWS_STORAGE_BUCKET_NAME}'

AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_USE_SSL = False

AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 300

MEDIA_URL = f"http://{AWS_S3_CUSTOM_DOMAIN}/"

AUTH_USER_MODEL = 'accounts.User'
