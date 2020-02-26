from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('add-site', views.add_site, name='add_site'),
    path('added-site', views.added_site, name='added_site'),
]