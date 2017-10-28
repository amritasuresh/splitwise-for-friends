# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from accounts.models import Account
from groups.forms import CreateGroupForm
from groups.models import UserGroup
import uuid


@login_required(login_url='/login')
def groups(request):
    account = Account.objects.get(user=request.user)
    subscribed_groups = request.user.groups.all()
    groups_data = []

    for group in subscribed_groups:
        users = User.objects.filter(groups__name=group.name)
        group_name = group.usergroup.group_name
        groups_data.append({'group_name': group_name, 'users': users})

    return render(request, 'sites/groups.html',
                  {'account': account, 'groups': groups_data})


def create_group_form(request):
    if request.method.upper() == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group_data = form.cleaned_data
            group_name = group_data["group_name"]

            # we generate unique name for django group by randomization
            unique_django_group_id = uuid.uuid4()

            while Group.objects.filter(name=unique_django_group_id).exists():
                unique_django_group_id = uuid.uuid4()

            group = Group.objects.create(name=unique_django_group_id)
            request.user.groups.add(group)
            group.user_set.add(request.user)

            UserGroup.objects.create(group=group, group_name=group_name,
                                     created=datetime.now())
        else:
            pass  # TODO

        return HttpResponseRedirect('/groups')
    else:
        return render(request, 'forms/create_group_form.html',
                      {'form': CreateGroupForm()})
