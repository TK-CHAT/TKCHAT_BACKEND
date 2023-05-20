"""
ASGI config for tkchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.livechat.routing

IS_DEV = 'RENDER' not in os.environ
CURRENT_ENV = 'local'if IS_DEV else'production'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tkchat.settings.'+CURRENT_ENV)
application = ProtocolTypeRouter({
  'http':get_asgi_application(),
  'websockets': AuthMiddlewareStack(
    URLRouter(
      apps.livechat.routing.websockets_urlpatterns
    )
  )
})
