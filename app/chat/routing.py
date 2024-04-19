from django.urls import re_path
from app.chat import consumers

websocket_urlpatterns = [
    re_path(r'^ws/halloween-vegan-backend/app/chat/$', consumers.ChatConsumer.as_asgi()),
]