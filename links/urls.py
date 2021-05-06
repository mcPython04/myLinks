from django.urls import path
from . import views
from django.conf.urls import include, url
from links.views import base
from django.contrib import admin
from .models import collection

urlpatterns = [ 
    path('home', views.home, name='home'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', base, name="base"),
    path('<str:username>', views.userPage, name="userPage"),
    path('links/update', views.linkUpdateView, name='updateLink'),
    path('links/create', views.LinkCreateView.as_view(), name='createLink'),
    path('links/create_collection', views.CollectionCreateView.as_view(), name='createCollection'),
    path('links/delete/<slug:pk>', views.LinkDeleteView.as_view(), name='deleteLink'),
    path('links/upload/<slug:pk>', views.LinkUploadView.as_view(), name='uploadLink'),
    path('links/collection/<slug:pk>', views.CollectionDetailView.as_view(), name='detailCollection'),
    path('links/collection/delete/<slug:pk>', views.CollectionDeleteView.as_view(), name='deleteCollection'),
    path('<str:username>/<str:collection_name>', views.collectionPage, name="collectionPage"),

]
