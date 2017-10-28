from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from groups import views
from .views import *

urlpatterns = [
    url(r'^groups/', groups),
    url(r'create_group_form', views.create_group_form, name='create_group_form')

]
