from pathlib import Path
import os
import re
import dj_database_url
from datetime import timedelta

if os.path.exists('env.py'):
    import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': CLOUDINARY_URL
}
MEDIA_URL = '/media/'
# MEDIA_URL = os.environ.get('MEDIA_URL')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %b %Y',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    #     # 'rest_framework.renderers.BrowsableAPIRenderer',
    # ],
}

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]


SPECTACULAR_SETTINGS = {
    'TITLE': 'LovinEscapades API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


if not DEBUG:
    REST_USE_JWT = True

# JWT configuration
SIMPLE_JWT = {
    'ALGORITHM': 'HS256',  # Common choice
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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# To use the API with React app: ALLOWED_HOST and CLIENT_ORIGIN_DEV in heroku
ALLOWED_HOSTS = [
    '127.0.0.1',
    '127.0.0.1:8000',
    'localhost',
]

# Application definition
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
    
    'drf_spectacular'
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


CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://localhost',
    "http://localhost:3000",
    'https://react-dj-restapi-eb6a7149ec97.herokuapp.com',
    'https://3000-eneliviu-reactdjrestapi-dm7huyvlcum.ws.codeinstitute-ide.net',
    'https://react-frontend-api-b166a083b609.herokuapp.com',
    'https://drf-backend-api-70211104c0c7.herokuapp.com'
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://localhost',
    "http://localhost:3000",
    'https://8000-eneliviu-djrestapi-vo4ia7gx81e.ws.codeinstitute-ide.net',
    'https://3000-eneliviu-reactdjrestapi-dm7huyvlcum.ws.codeinstitute-ide.net',
    'https://react-frontend-api-b166a083b609.herokuapp.com/signup',
    'https://drf-backend-api-70211104c0c7.herokuapp.com/'
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


# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
# else:
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set the maximum file upload size to 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB in bytes

# Set the maximum request body size to 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB in bytes

# Define a custom maximum upload size for use in validation
MAX_UPLOAD_SIZE = 10485760  # 10 MB in bytes
