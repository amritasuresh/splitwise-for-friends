# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from accounts.models import Account
from groups.forms import CreateGroupForm, AddUserToGroupForm, \
    AddTransactionToGroupForm
from groups.models import UserGroup
from transactions.models import Transaction
import uuid


@login_required(login_url='/login')
def groups(request):
    my_account = Account.objects.get(user=request.user)
    subscribed_groups = request.user.groups.all()
    groups_data = []

    for grp in subscribed_groups:
        users = User.objects.filter(groups__name=grp.name)
        group_name = grp.usergroup.group_name
        group_id = grp.usergroup.id
        groups_data.append(
            {'group_name': group_name, 'users': users, 'id': group_id})

    return render(request, 'sites/groups.html',
                  {'my_account': my_account, 'groups': groups_data})


@login_required(login_url='/login')
def group(request, usergroup_id):
    print(usergroup_id)
    try:
        usergroup = UserGroup.objects.get(id=usergroup_id)
    except UserGroup.DoesNotExist:
        usergroup = None  # TODO invalid usergroup_id

    my_account = Account.objects.get(user=request.user)
    users = User.objects.filter(groups__name=usergroup.group.name)

    transactions = Transaction.objects.filter(group_id=usergroup_id)

    return render(request, 'sites/group.html',
                  {'my_account': my_account, 'usergroup': usergroup,
                   'users': users, 'transactions': transactions})


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def add_user_to_group_form(request, usergroup_id):
    if request.method.upper() == "POST":
        form = AddUserToGroupForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            username = user_data["username"]

            grp = UserGroup.objects.get(id=usergroup_id).group
            user = User.objects.get(username=username)
            user.groups.add(grp)


        else:
            pass  # TODO

        return HttpResponseRedirect('/groups/group' + str(usergroup_id))
    else:
        return render(request, 'forms/add_user_to_group_form.html',
                      {'form': AddUserToGroupForm(),
                       "usergroup_id": usergroup_id})


@login_required(login_url='/login')
def add_transaction_to_group_form(request, usergroup_id):
    try:
        usergroup = UserGroup.objects.get(id=usergroup_id)
    except UserGroup.DoesNotExist:
        usergroup = None  # TODO invalid usergroup_id

    users = User.objects.filter(groups__name=usergroup.group.name)

    if request.method.upper() == "POST":
        form = AddTransactionToGroupForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            transaction = user_data["transaction"]
            payer = user_data["payer"]
            details = user_data["details"]

            grp = UserGroup.objects.get(id=usergroup_id)
            payer_user = User.objects.get(username=payer)
            payer_account = Account.objects.get(user_id=payer_user.id)
            num_of_users = users.count()
            amount = float(transaction) / num_of_users

            for user in users:
                if user.id != payer_user.id:
                    user_account = User.objects.get(username=user)
                    account = Account.objects.get(user_id=user_account.id)
                    Transaction.objects.create(name=details, payee=account,
                                               payer=payer_account,
                                               amount=amount, group=grp,
                                               created=datetime.now())

        else:
            pass  # TODO

        return HttpResponseRedirect('/groups/group' + str(usergroup_id))
    else:
        return render(request, 'forms/add_transaction_to_group_form.html',
                      {'form': AddTransactionToGroupForm(),
                       "usergroup_id": usergroup_id})
