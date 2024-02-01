from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),
    path('ws/sc/<str:groupname>/', consumers.MySyncConsumer.as_asgi()),
]