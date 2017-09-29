from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import home, register

urlpatterns = [
    url(r'^$', home),
    url(r'^register/', register),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'})
]
