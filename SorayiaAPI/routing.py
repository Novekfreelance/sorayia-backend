from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from app import consumers

websocket_urlpatterns = [
    path('ws/chat/<room_id>', consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket':  URLRouter(
                websocket_urlpatterns
            ),
})
