from .base import *

DEBUG = False


SECURE_SSL_REDIRECT = False
SECURE_REDIRECT_EXEMPT = []

# when true cookie only through https
SESSION_COOKIE_SECURE = True
# cookie will be marked as “secure”
CSRF_COOKIE_SECURE = True


ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass
