"""NyovePortfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from home import views

urlpatterns = [
    path('', views.index),
    path('bug', views.bug),
    path('login', views.login),
    path('admin', views.admin),
    path('logout', views.logout),
    path('api/addImg', views.addImg),
    path('api/addBug', views.addBug),
    path('api/actionImg', views.actionImg),
    path('api/actionBug', views.actionBug),
    path('admin/bug', views.changeBug),
    path('admin/img', views.changeImg),
    path('api/changeBug', views.changeBugApi),
    path('api/changeImg', views.changeImgApi),
]
