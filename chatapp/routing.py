# routing.py

from django.urls import re_path,path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/<str:username>/',ChatConsumer.as_asgi()),
]
