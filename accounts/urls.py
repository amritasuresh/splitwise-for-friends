from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    url(r'^$', home),
    url(r'^register/', register),
    url(r'^forgotpassword/', forgot_password),
    url(r'^login/$', auth_views.login, {'template_name': 'sites/login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name': 'sites/logout.html'})
]
