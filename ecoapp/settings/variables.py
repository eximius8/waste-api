import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# For other apps
SITE_ID=1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DB keys
POSTGR_WASTE_USER = os.environ.get('POSTGR_WASTE_USER')
POSTGR_WASTE_USER_PASS = os.environ.get('POSTGR_WASTE_USER_PASS')

# age of connect ion to db
CONN_MAX_AGE = 1000

SESSION_COOKIE_AGE = 600000

# GCP credentials 
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')) 




# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Wagtail settings
WAGTAIL_EMAIL_MANAGEMENT_ENABLED = False
WAGTAIL_ALLOW_UNICODE_SLUGS = False
# Wagtail settings
WAGTAIL_SITE_NAME = "ecoapp"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'
AUTH_USER_MODEL = 'auth.User'


# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
#BASE_URL = 'https://ru.bezoder.com'
