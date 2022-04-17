from django.contrib import admin
from django.urls import path
from YCAML import views

urlpatterns = [
    path('', views.index,name='YCAML'),
    path('index', views.index,name='YCAML'),
    path('deepanalyser', views.deepanalyser),
]
