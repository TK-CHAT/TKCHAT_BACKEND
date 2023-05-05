"""
WSGI config for tkchat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
IS_DEV = 'RENDER' not in os.environ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tkchat.settings.'+'local'if IS_DEV else'production')

application = get_wsgi_application()
