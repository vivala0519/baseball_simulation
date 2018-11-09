from django.conf.urls import url

from . import player

websocket_urlpatterns = [
    # url(r'^ws/game/(?P<room_name>[^/]+)/$', player.ChatConsumer),

    url(r'^ws/(?P<room_name>[^/]+)/$', player.ChatConsumer),
]