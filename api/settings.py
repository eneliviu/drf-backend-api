from pathlib import Path
import os
from datetime import timedelta
# import re
import dj_database_url


if os.path.exists('env.py'):
    import env

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': CLOUDINARY_URL
}
MEDIA_URL = '/media/'
# MEDIA_URL = os.environ.get('MEDIA_URL')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
SECRET_KEY = os.getenv('SECRET_KEY')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %b %Y',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]
else:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ]


SPECTACULAR_SETTINGS = {
    'TITLE': 'LovinEscapades API',
    'DESCRIPTION': 'Trip sharing platform API for LovinEscapades',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

REST_USE_JWT = True

SIMPLE_JWT = {
    'ALGORITHM': 'HS256',
    'AUTH_COOKIE': 'jwt-auth',
    'AUTH_COOKIE_SECURE': not DEBUG,  # local dev False, True for production
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'Lax',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,  # Update last_login field on token issue
}

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG  # False for local dev, True for production

CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = False  # Must be False for frontend access
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG  # False for local dev, True for production

REST_AUTH = {
    'USER_DETAILS_SERIALIZER': 'api.serializers.CurrentUserSerializer'
}

LOGIN_REDIRECT_URL = '/'

# To use the API with React app: ALLOWED_HOST and CLIENT_ORIGIN_DEV in heroku
ALLOWED_HOSTS = [
    '127.0.0.1',
    '127.0.0.1:8000',
    '127.0.0.1:3000',
    'localhost',
    'dj-api-backend-8cf355e96add.herokuapp.com'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'cloudinary',
    'cloudinary_storage',
    'django.contrib.staticfiles',

    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    'profiles',
    'trips',
    'likes',
    'followers',

    'drf_spectacular',
    'django_extensions',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
  'app_labels': ["profiles", "trips", "likes", "followers"],
}

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://localhost',
    "http://localhost:3000",
    'https://react-dj-restapi-eb6a7149ec97.herokuapp.com',
    'https://react-frontend-api-b166a083b609.herokuapp.com',
    'https://dj-api-backend-8cf355e96add.herokuapp.com'
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://localhost',
    "http://localhost:3000",
    'https://react-frontend-api-b166a083b609.herokuapp.com/signup',
    'https://drf-backend-api-70211104c0c7.herokuapp.com'
]

ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL)
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASE_URL = os.environ.get('DATABASE_URL')
# DATABASES = {
#     "default": dj_database_url.config(default=DATABASE_URL)
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
                    'django.contrib.auth.password_validation.'
                    'UserAttributeSimilarityValidator'
                ),
    },
    {
        'NAME': (
                    'django.contrib.auth.password_validation.'
                    'MinimumLengthValidator'
                ),
    },
    {
        'NAME': (
                    'django.contrib.auth.password_validation.'
                    'CommonPasswordValidator'
                ),
    },
    {
        'NAME': (
                    'django.contrib.auth.password_validation.'
                    'NumericPasswordValidator'
                ),
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
MAX_UPLOAD_SIZE = 10485760
