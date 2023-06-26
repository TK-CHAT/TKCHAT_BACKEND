"""
ASGI config for tkchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
IS_DEV = 'RENDER' not in os.environ
CURRENT_ENV = 'local'if IS_DEV else'production'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tkchat.settings.'+CURRENT_ENV)
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from .urls import urlpatterns
import apps.livechat.routing


application = ProtocolTypeRouter({
  'http':AsgiHandler(),
  'websocket': URLRouter(apps.livechat.routing.websockets_urlpatterns),
})
