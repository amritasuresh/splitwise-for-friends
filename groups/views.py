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
from groups.forms import ResolveTransactions
from groups.models import UserGroup
from transactions.models import Transaction
import uuid
import operator


@login_required(login_url='/login')
def groups(request):
    """
    This view shows the list of groups that the current user belongs to.
    :param request: HttpRequest object
    :return: The rendered groups.html page.
    """
    my_account = Account.objects.get(user=request.user)
    subscribed_groups = request.user.groups.all()
    groups_data = []

    for grp in subscribed_groups:
        users = User.objects.filter(groups__name=grp.name)
        group_name = grp.usergroup.group_name
        group_id = grp.usergroup.id
        transactions = Transaction.objects.filter(group_id=grp.usergroup.id)
        number_of_transactions = transactions.count()
        total_money = sum([transaction.amount for transaction in transactions])

        groups_data.append(
            {
                'group_name': group_name,
                'users': users,
                'id': group_id,
                'number_of_transactions': number_of_transactions,
                'total_money': total_money
            }
        )

    return render(request, 'sites/groups.html',
                  {'my_account': my_account, 'groups': groups_data,
                   'add_group_form': CreateGroupForm()})


@login_required(login_url='/login')
def group(request, usergroup_id):
    """
    This view shows the details pertaining to a given group, including transaction history and members.
    :param request: HttpRequest object
    :param usergroup_id: The unique UUID of the group
    :return: The rendered group.html page
    """
    try:
        usergroup = UserGroup.objects.get(id=usergroup_id)
    except UserGroup.DoesNotExist:
        usergroup = None  # TODO invalid usergroup_id

    my_account = Account.objects.get(user=request.user)
    users = User.objects.filter(groups__name=usergroup.group.name)

    transactions = Transaction.objects.filter(group_id=usergroup_id)

    return render(request, 'sites/group.html',
                  {'my_account': my_account, 'usergroup': usergroup,
                   'users': users, 'transactions': transactions,
                   'resolve_form': ResolveTransactions(),
                   'transaction_form': AddTransactionToGroupForm()})


@login_required(login_url='/login')
def create_group_form(request):
    """
    This view creates a form for adding a new group.
    :param request: HttpRequest object
    :return: The groups.html page if the group was successfully added, or the create_group_form.html page if not
    """
    if request.method.upper() == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group_data = form.cleaned_data
            group_name = group_data["group_name"]

            # we generate unique name for django group by randomization
            unique_django_group_id = uuid.uuid4()

            while Group.objects.filter(name=unique_django_group_id).exists():
                unique_django_group_id = uuid.uuid4()

            grp = Group.objects.create(name=unique_django_group_id)
            request.user.groups.add(grp)
            grp.user_set.add(request.user)

            UserGroup.objects.create(group=grp, group_name=group_name,
                                     created=datetime.now())
        else:
            pass  # TODO

        return HttpResponseRedirect('/groups')
    else:
        return render(request, 'forms/create_group_form.html',
                      {'form': CreateGroupForm()})


@login_required(login_url='/login')
def add_user_to_group_form(request, usergroup_id):
    """
    This view adds a user to an existing group.
    :param request: HttpRequest object
    :param usergroup_id: The unique UUID of the group
    :return: The rendered page of the group if successful, and the add_user_to_group_form.html page if not.
    """
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

        return HttpResponseRedirect('/groups/' + str(usergroup_id))
    else:
        return render(request, 'forms/add_user_to_group_form.html',
                      {'form': AddUserToGroupForm(),
                       "usergroup_id": usergroup_id})


@login_required(login_url='/login')
def add_transaction_to_group_form(request, usergroup_id):
    """
    This view adds a transaction to an existing group.
    :param request: HttpRequest object
    :param usergroup_id: The unique UUID of the group.
    :return: The rendered page of the group if successful, and the add_transaction_to_group_form.html page if not.
    """
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

        return HttpResponseRedirect('/groups/' + str(usergroup_id))
    else:
        return render(request, 'forms/add_transaction_to_group_form.html',
                      {'form': AddTransactionToGroupForm(), 'usergroup_id': usergroup_id})


@login_required(login_url='/login')
def resolve_transactions(request, usergroup_id):
    try:
        usergroup = UserGroup.objects.get(id=usergroup_id)
    except UserGroup.DoesNotExist:
        usergroup = None  # TODO invalid usergroup_id
    if request.method.upper() == "POST":
        form = ResolveTransactions(request.POST)
        users = User.objects.filter(groups__name=usergroup.group.name)
        if form.is_valid():
            user_data = form.data
            resolution_type = user_data["resolutiontype"]
            useramount_list = {}
            for user in users:
                useramount_list[user.username]=0
            transactions = Transaction.objects.filter(group_id=usergroup_id, status='O')
            for transaction in transactions:
                if transaction.name == 'resolution':
                    useramount_list[transaction.payer.user.username] -= transaction.amount
                    useramount_list[transaction.payee.user.username] += transaction.amount
                else:
                    useramount_list[transaction.payee.user.username] -= transaction.amount
                    useramount_list[transaction.payer.user.username] += transaction.amount
            updateTransactions = Transaction.objects.filter(group_id=usergroup_id).update(status='C')
                #transaction.status = 1;
            if resolution_type == "opt_tran":
                print('You have chosen to optimize overall transactions')
                sorted_transaction_list = sorted(useramount_list.items(), key=operator.itemgetter(1))
                optimize_by_transaction(sorted_transaction_list, usergroup)


            else:
                print('You have chosen to optimize per user')
        else:
            pass #TODO

        return HttpResponseRedirect('/groups/' + str(usergroup_id))
    else:
        return render(request, 'forms/resolve_group_expenses_form.html',
                      {'form': ResolveTransactions(), 'usergroup_id': usergroup_id})


def optimize_by_transaction(sorted_transaction_list, usergroup):
    def getKey(item):
        return item[1]
    sorted_transaction_list = sorted(sorted_transaction_list, key=getKey)
    first_key = sorted_transaction_list[0][0]
    first_value = sorted_transaction_list[0][1]
    firstTup = (first_key, first_value)
    first_value = first_value*-1
    last_key = sorted_transaction_list[sorted_transaction_list.__len__()-1][0]
    last_value = sorted_transaction_list[sorted_transaction_list.__len__()-1][1]
    if first_value == 0 and last_value == 0:
        return
    lastTup = (last_key, last_value)
    if first_value > last_value and sorted_transaction_list.__len__()>0:
        payer = User.objects.get(username=first_key)
        payee = User.objects.get(username=last_key)
        Transaction.objects.create(name='resolution', payee=Account.objects.get(user=payee),
                                       payer=Account.objects.get(user=payer),
                                       amount=last_value,
                                       group=usergroup,
                                       created=datetime.now())
        sorted_transaction_list.remove(lastTup)
        sorted_transaction_list.remove(firstTup)
        newTup = (first_key, last_value-first_value)
        sorted_transaction_list.append(newTup)
        optimize_by_transaction(sorted_transaction_list, usergroup)
    else:
        payer = User.objects.get(username=first_key)
        payee = User.objects.get(username=last_key)
        Transaction.objects.create(name='resolution', payee=Account.objects.get(user=payee),
                                   payer=Account.objects.get(user=payer),
                                   amount=first_value,
                                   group=usergroup,
                                   created=datetime.now())
        sorted_transaction_list.remove(firstTup)
        sorted_transaction_list.remove(lastTup)
        newTup = (last_key, last_value-first_value)
        sorted_transaction_list.append(newTup)
        optimize_by_transaction(sorted_transaction_list, usergroup)

