from .base import *

DEBUG = False


SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = []

# when true cookie only through https
SESSION_COOKIE_SECURE = True
# cookie will be marked as “secure”
CSRF_COOKIE_SECURE = True

# https://stackoverflow.com/questions/49166768/setting-secure-hsts-seconds-can-irreversibly-break-your-site
# check deploy says to do it:
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_AGE = 600000


ALLOWED_HOSTS = [
    '.appspot.com',
    '.api.ma34.ru',
]

# DRF CORS settings
#CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS 
CORS_ALLOWED_ORIGINS = [
    "https://ma34.ru",
    "https://www.ma34.ru",    
    "https://bezoder.firebaseapp.com",
    "https://38o6y.csb.app",
]

#CORS_ALLOWED_ORIGIN_REGEXES = []

try:
    from .local import *
except ImportError:
    pass

#python manage.py check --deploy --settings=ecoapp.settings.production
