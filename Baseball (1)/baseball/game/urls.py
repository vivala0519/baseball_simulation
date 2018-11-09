from django.conf.urls import url
from django.urls import path


from . import views

urlpatterns = [
    path('SearchPlayer/', views.SearchPlayer),

    # r'^$'를 입력했더니 소켓 연결됨. 그전에 연결이 안됐었나봄....
    url(r'^$', views.home, name='home'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    path('SearchPlayer/', views.SearchPlayer),

]