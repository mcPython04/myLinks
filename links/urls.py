from django.urls import path
from . import views
from django.conf.urls import include, url
from links.views import base
from django.contrib import admin

urlpatterns = [
    path('home/<str:username>', views.home, name='home'),
    path('add/', views.add_view, name='add'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',base,name="base"),
    path('dashboard/',views.dashboard,name="dashboard"),
    #path('admin/', admin.site.urls,name="admin"),
]   