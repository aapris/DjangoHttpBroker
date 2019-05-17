import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbname',  # Or path to database file if using sqlite3.
        'USER': 'username',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'broker',  # Contains URL routing, model for
    'demoplugin',  # Just some default endpoints for demonstration purposes
]

# RabbitMQ
RABBITMQ_APP = 'myapp'
RABBITMQ = {
    'ROUTING_KEY_PREFIX': RABBITMQ_APP,  # Override in local_settings
    'HOST': 'localhost',
    'VHOST': f'/{RABBITMQ_APP}',  # If you have just one instance running on the server, use '/'
    'PORT': 5672,
    'USER': None,
    'PASSWORD': None,
}
