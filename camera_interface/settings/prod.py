from .base import *
import os
DEBUG = os.getenv("DEBUG") == "0"

ADMINS = [
    ('Vitalii l', 'meff86@list.ru'),
]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": os.environ.get('MYSQL_DATABASE'),
        "USER": os.environ.get('MYSQL_USER'),
        "HOST": 'db',
        "PORT": 3306,
        "PASSWORD": os.environ.get('MYSQL_PASSWORD'),
    }
}