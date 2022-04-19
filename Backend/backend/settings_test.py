import os

from .settings import *

local = os.getenv('local')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_test',
        'TEST': {
            'NAME': 'django_db_for_test',
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        },
        'USER': 'root',
        'PASSWORD': 'password_for_test',
        'HOST': 'db-test' if not local else 'localhost',
        'PORT': '3306'
    }
}
