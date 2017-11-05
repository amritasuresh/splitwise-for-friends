from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
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
    # profile pages
    url(r'^profilepage/$', profile_page),
    url(r'^user/(?P<user_id>[0-9]+)/$', user_page),
]