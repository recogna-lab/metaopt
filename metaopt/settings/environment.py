from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j2n06l=2((_bfzb$3uy=1*^_68z%m7_&wc=dcngui2j9n$f!et'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

ROOT_URLCONF = 'metaopt.urls'

CSRF_FAILURE_VIEW = 'metaopt.views.custom_csrf_failure'

WSGI_APPLICATION = 'metaopt.wsgi.application'