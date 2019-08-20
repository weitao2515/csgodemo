from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("search/",views.search),
    path("match/",views.match),
    path("demo/",views.demo),
]