from django.urls import path
from . import views

urlpatterns = [
    path('static_link/create', views.StaticCreateView.as_view(), name='createStatic')
]
