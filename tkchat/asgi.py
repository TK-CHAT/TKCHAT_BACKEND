"""
ASGI config for tkchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


IS_DEV = 'RENDER' not in os.environ

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tkchat.settings.'+'local' if IS_DEV else 'production')

application = get_asgi_application()
