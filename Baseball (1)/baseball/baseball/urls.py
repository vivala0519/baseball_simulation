"""baseball URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from .views import UserCreateView, UserCreateDoneTV
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # 장고가 제공하는 인증과 url 형식 사용 / account 하위 주어줌 / 로그인인 경우 :8000/acounts/login/
    path('accounts/register/', UserCreateView.as_view(), name='register'),  # 계정을 추가(생성)하는 뷰 URL
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'),  # 계정 생성이 완료되니 후 보여줄 뷰 URL
    path('', HomeView.as_view(), name='home'),

    path('game/', include('game.urls')),


]
