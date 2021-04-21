from django.urls import path
from . import views
from django.conf.urls import include, url
from links.views import base
from django.contrib import admin

urlpatterns = [
    path('home', views.home, name='home'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',base,name="base"),
    path('<str:username>', views.userPage,name="userPage"),
]   