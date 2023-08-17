from .base import *


DEBUG = os.getenv("DEBUG") == "1"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
        "PASSWORD": POSTGRES_PASSWORD,
    }
}