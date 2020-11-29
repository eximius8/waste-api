from .base import *

DEBUG = False


SECURE_SSL_REDIRECT = False
SECURE_REDIRECT_EXEMPT = []

# when true cookie only through https
SESSION_COOKIE_SECURE = True
# cookie will be marked as “secure”
CSRF_COOKIE_SECURE = True


ALLOWED_HOSTS = [
    '.appspot.com',
    '.api.ma34.ru',
]

# DRF CORS settings
#CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "https://ma34.ru",
    "https://www.ma34.ru",
    "https://bezoder.web.app",
    "https://bezoder.firebaseapp.com/",
    "https://38o6y.csb.app",
]

try:
    from .local import *
except ImportError:
    pass
