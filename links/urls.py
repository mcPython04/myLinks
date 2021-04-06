from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('links/<int:link_id>/upload/', views.image_upload_view),
    path('links/add/', views.add_view),
]   