from _core.settings.base import *

DEBUG = True
ALLOWED_HOSTS = []

EMAIL_HOST = '0.0.0.0'
EMAIL_PORT = '1025'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
