from django.conf.urls import url
from django.urls import path


from . import views

urlpatterns = [
    # r'^$'를 입력했더니 소켓 연결됨. 그전에 연결이 안됐었나봄....
    path('', views.room, name='home'),
    path('SearchPlayer/', views.SearchPlayer),
    path('searchByYear/', views.searchByYear),
    path('getBatters/', views.getBatters),
    path('getPitchers/', views.getPitchers),
]