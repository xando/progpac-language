import os
BASE_DIR = os.path.dirname(__file__)
SECRET_KEY = 'w=9isj!4!m=)8eqfhrnb8!c34-y3#1qt*i!-!f1dyinh&mt@z-'

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    # 'django.contrib.staticfiles',
    'progpac',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'progpac.urls'
WSGI_APPLICATION = 'progpac.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
