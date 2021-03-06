from django.urls import path
from . import views

urlpatterns = [
    path('static_link/create', views.StaticCreateView.as_view(), name='createStatic'),
    path('static_link/search', views.SearchResultsView.as_view(), name='search_results'),
    path('static_link/<str:name>', views.static_link_page, name='pageStatic'),
]
