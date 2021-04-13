from django.urls import path
from . import views
from django.conf.urls import include, url
from links.views import dashboard, base


urlpatterns = [
    path('index/', views.index_view, name='index'),
    #path('add/', views.add_view, name='add'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',base,name="base"),
    path('dashboard/',dashboard,name="dashboard"),

]   