from unicodedata import name
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from django.conf.urls import  url

from NanoPayApp import views
from drf_yasg import openapi


router = DefaultRouter() 

urlpatterns = [ ]