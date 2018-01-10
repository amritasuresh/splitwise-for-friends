
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from groups import views
from .views import *

urlpatterns = [
    # groups
    url(r'^groups/$', groups),

    # single group
    url(r'^groups/(?P<usergroup_id>[0-9A-Fa-f-]+)/$', views.group),
    url(r'^groups/(?P<usergroup_id>[0-9A-Fa-f-]+)/events/(?P<event_id>[0-9A-Fa-f-]+)/$', views.event),
    url(r'^groups/(?P<usergroup_id>[0-9A-Fa-f-]+)/events/(?P<event_id>[0-9A-Fa-f-]+)/deleteevent/$', views.delete_event),
    url(r'^groups/(?P<usergroup_id>[0-9A-Fa-f-]+)/adduser',
        views.add_user_to_group_form),
    url(r'^groups/(?P<usergroup_id>[0-9A-Fa-f-]+)/addtransaction',
        views.add_transaction_to_group_form),
    url(r'^groups/(?P<usergroup_id>[0-9A-Fa-f-]+)/addcustomtransaction',
        views.add_custom_transaction_to_group_form),
    url(r'^groups/(?P<usergroup_id>[0-9A-Fa-f-]+)/createevent',
        views.create_event_form),
    url(r'^groups/(?P<usergroup_id>[0-9A-Fa-f-]+)/resolve',
        views.resolve_transactions),

    # forms:
    url(r'^groups/create_group_form', views.create_group_form, name='create_group_form'),
]