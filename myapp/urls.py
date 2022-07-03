
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('upload/', views.uploadView),
    path('search/', views.searchView),
    path('update/', views.updateView),
    path('', views.appView)
]
