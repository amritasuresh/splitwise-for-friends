from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts import views
from .views import *


urlpatterns = [
    # home
    url(r'^$', home),
    # registration
    url(r'^register/$', register),
    url(r'^forgotpassword/$', forgot_password),
    # login/logout
    url(r'^login/$', auth_views.login, {'template_name': 'sites/login.html'}),
    url(r'^logout/$', auth_views.logout),
    # users
    url(r'^users/$', users),
    url(r'^users/friends/$', friends),
    # profile pages
    url(r'^profile/$', profile_page),
    url(r'^settings/$', settings),
    url(r'^settings/save/$', views.save_settings),
    url(r'^users/(?P<user_id>[0-9]+)/$', user_page),
    # settings change
    url(r'^settings_change/$', settings_change),
]