"""
ASGI config for halloween_vegan_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import app.chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.halloween_vegan_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app.chat.routing.websocket_urlpatterns  # WebSocket маршруты
        )
    ),
})
