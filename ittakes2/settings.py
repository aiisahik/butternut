import os
import dj_database_url
import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '85a$2a#((e6t5(+&u=76ckxz-^pak&kg5^w7(0q-qq7mlv=4f!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOCAL_ENV = os.environ.get('LOCAL_ENV', False)

ALLOWED_HOSTS = ['*']


# Cache setup   - Redis
if LOCAL_ENV:
    CACHES = {
        'default': {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/0",
            "OPTIONS": {
                'DB': 1,
                # "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            }
        }
    }
    DATABASES = {
        'default': {
            'PASSWORD': 'c0euVzU6CWiiJPlz8DLHV9Yxdv',
            'PORT': 5432,
            'HOST': 'ec2-54-204-0-120.compute-1.amazonaws.com',
            'USER': 'hdldkfrpjsrhjz',
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'd8t41ts7gv55rs'
        }
    }
else: 
    DATABASES = {
        'default':  dj_database_url.config()
    }
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
    CACHES = {
            'default': {
                'BACKEND': 'redis_cache.RedisCache',
                'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
                'OPTIONS': {
                    'PASSWORD': redis_url.password,
                    'DB': 0,
            }
        }
    }
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ittakes2.account',
    'ittakes2.matches',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'ittakes2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'ittakes2/templates'),
            os.path.join(BASE_DIR, 'ittakes2/templates/base'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ittakes2.context_processors.basic_info',
            ],
        },
    },
]
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )

WSGI_APPLICATION = 'ittakes2.wsgi.application'


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'ittakes2/static'),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
