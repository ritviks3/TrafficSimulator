from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from trafficapp.consumers import ChatConsumer
application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/trafficapp/', ChatConsumer.as_asgi()),
    ])
})