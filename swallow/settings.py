"""
Django settings for swallow project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1+-&ds0jx%6$#2*7clbmfq)i=aqwo4w&1ipx9osqhjz^@lqse3'

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
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'idc',
    'manufactory',
    'supplier',
    'server',
    'permcontrol',
    'uposition'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'swallow.urls'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

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

WSGI_APPLICATION = 'swallow.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swallow',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'db',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
AUTH_USER_MODEL = "permcontrol.User"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'apps.core.permissions.CustomPermissions',
    ),
}

# celery settting
# celery中间件 redis://redis服务所在的ip地址:端口/数据库号
BROKER_URL = 'redis://redis-server'

# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://redis-server'

CELERY_QUEUES = {
    'beat_autoServer': {
        'exchange': 'beat_autoServer',
        'exchange_type': 'direct',
        'binding_key': 'beat_autoServer'
    },
    'work_queue': {
        'exchange': 'work_queue',
        'exchange_type': 'direct',
        'binding_key': 'work_queue'
    }
}
CELERY_DEFAULT_QUEUE = 'work_queue'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# celery时区设置
CELERY_TIMEZONE = 'Asia/Shanghai'

# 有些情况可以防止死锁
CELERY_FORCE_EXECV = True

# 允许重试
CELERY_ACKS_LATE = True

# 每个worker最多执行100个任务后被销毁，防止内存泄露
CELERY_MAX_TASKS_PER_CHILD = 100

# 单个任务的最大运行时间
CELERY_TASK_TIME_LIMIT = 12 * 30

# 设置并发的worker数量
# CELERY_CONCURRENCY = 4

# 定时更新服务器配置时间，默认为15分钟
CELERYBEAT_SCHEDULE = {
    'autoServer': {
        'task': 'auto_server',
        'schedule': crontab(minute='*/1'),
        'args': (),
        'options': {
            'queue': 'beat_autoServer'
        }
    }
}

# requests 设置
# 管理员用户
REQUEST_USERNAME = 'admin'
# 管理员用户密码
REQUEST_PASSWORD = 'admin123456'

REQUEST_TOKEN_URL = 'http://127.0.0.1:8000/api-token-auth/'

REQUEST_AUTOSERVER_URL = 'http://127.0.0.1:8000/serverauto/'

# Ansible 设置
# Ansible Inventory
ANSIBLE_HOSTS_FILE = '/etc/ansible/hosts'

# 需要定时更新服务器资源的用户组
ANSIBLE_GROUP = "swallow_servers"
