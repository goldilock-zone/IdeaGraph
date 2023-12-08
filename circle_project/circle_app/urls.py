# circle_app/urls.py
from django.urls import path
from . import views
from .views import display_html_file

urlpatterns = [
    path('', views.home, name='home'),
    path('circle/', views.circle_page, name='circle_page'),
    path('temp/', views.display_html_file, name='temp'),
    path('add/', views.add_page, name='add'),
    path('del/', views.del_page, name='del'),
    path('create/', views.create_node, name='create_node'),
    path('list/', views.node_list, name='node_list')
]
