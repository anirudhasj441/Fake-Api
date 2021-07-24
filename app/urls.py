from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('clients',views.clients,name="get_clients"),
    path('clients/projects', views.projects),
    path('projects', views.projects),
    path('login',views.user_login),
    path('logout', views.user_logout)
]