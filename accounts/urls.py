from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounting_for_friends import settings
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', home),
    url(r'^register/$', register),
    url(r'^forgotpassword/$', forgot_password),
    url(r'^users/$', users),
    url(r'^profilepage/$', profile_page),
    url(r'^login/$', auth_views.login, {'template_name': 'sites/login.html'}),
    url(r'^logout/$', auth_views.logout)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)