# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts.models import Account
from events.models import Event

from currencies.views import convert_amount, amount_as_string

from groups.forms import CreateGroupForm, AddUserToGroupForm, AddTransactionToGroupForm, CreateEventForm
from groups.forms import ResolveTransactions, AddCustomTransactionToGroupForm
from groups.models import UserGroup

from transactions.models import Transaction

import uuid, operator, decimal


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

        total = 0.0
        for t in transactions:
            amount = convert_amount(request, t.amount, t.currency, my_account.currency)
            total += float(format(amount, '.2f'))

        total_money = amount_as_string(request, total, my_account)

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
    events = Event.objects.filter(group_id=usergroup_id)
    form = AddTransactionToGroupForm()
    form.fields["payer"].queryset = User.objects.filter(groups__name=usergroup.group.name)
    custom_transaction = AddCustomTransactionToGroupForm()
    custom_transaction.fields["payer"].queryset = User.objects.filter(groups__name=usergroup.group.name)
    #custom_transaction.fields["payee"].queryset = User.objects.filter(groups__name=usergroup.group.name)
    payee_user = [str(payee_name) for payee_name in User.objects.filter(groups__name=usergroup.group.name)]
    custom_transaction.fields["consumers"].choices=[(payee_name, payee_name) for payee_name in payee_user]
    #query = User.objects.filter(groups__name=usergroup.group.name)

    for t in transactions:
        amount = convert_amount(request, t.amount, t.currency, my_account.currency)
        t.amount = float(format(amount, '.2f'))

    transaction_strings = []
    for t in transactions:
        transaction_strings.append(amount_as_string(request, t.amount, my_account))

    list = zip(transactions, transaction_strings)

    return render(request, 'sites/group.html',
                  {'my_account': my_account, 'usergroup': usergroup,
                   'users': users, 'transactions': list,
                   'events': events,
                   'resolve_form': ResolveTransactions(),
                   'transaction_form': form,
                   'custom_transaction_form' : custom_transaction,
                   'user_add_form': AddUserToGroupForm(),
                   'create_event_form': CreateEventForm()})


@login_required(login_url='/login')
def event(request, usergroup_id, event_id):
    """
    This view shows the details about a particular Event, including the associated transactions.
    :param request: The HTTP request
    :param usergroup_id: The unique ID of the group to which the Event belongs
    :param event_id: The unique ID of the Event
    :return: The rendered event.html page
    """
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = None  # TODO invalid event

    my_account = Account.objects.get(user=request.user)
    usergroup = UserGroup.objects.get(id=usergroup_id)
    transactions = Transaction.objects.filter(event_id=event_id)

    for t in transactions:
        amount = convert_amount(request, t.amount, t.currency, my_account.currency)
        t.amount = float(format(amount, '.2f'))

    transaction_strings = []
    for t in transactions:
        transaction_strings.append(amount_as_string(request, t.amount, my_account))

    list = zip(transactions, transaction_strings)

    return render(request, 'sites/event.html',
                  {'my_account': my_account, 'usergroup': usergroup,
                   'event': event,
                   'transactions': list})

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
        form = AddTransactionToGroupForm(data=request.POST)
        user_data = form.data
        transaction = user_data["transaction"]
        payer = user_data["payer"]
        details = user_data["details"]
        event_id = user_data["event"]

        grp = UserGroup.objects.get(id=usergroup_id)
        payer_user = User.objects.get(id=payer)
        payer_account = Account.objects.get(user_id=payer_user.id)
        event = Event.objects.get(id=event_id)
        num_of_users = users.count()
        amount = float(transaction) / num_of_users

        for user in users:
            if user.id != payer_user.id:
                user_account = User.objects.get(username=user)
                account = Account.objects.get(user_id=user_account.id)
                Transaction.objects.create(name=details, payee=account,
                                           payer=payer_account,
                                           amount=amount, group=grp,
                                           event=event,
                                           created=datetime.now())

            else:
                pass  # TODO

        return HttpResponseRedirect('/groups/' + str(usergroup_id))
    else:
        form = AddTransactionToGroupForm()
        form.fields["payer"].queryset = User.objects.filter(groups__name=usergroup.group.name)
        return render(request, 'forms/add_transaction_to_group_form.html',
                      {'form': form, 'usergroup_id': usergroup_id})

@login_required(login_url='/login')
def add_custom_transaction_to_group_form(request, usergroup_id):
    """
    This view adds a custom transaction to an existing group.
    :param request: HttpRequest object
    :param usergroup_id: The unique UUID of the group.
    :return: The rendered page of the group if successful, and the add_custom_transaction.html page if not.
    """
    try:
        usergroup = UserGroup.objects.get(id=usergroup_id)
    except UserGroup.DoesNotExist:
        usergroup = None  # TODO invalid usergroup_id

    users = User.objects.filter(groups__name=usergroup.group.name)

    if request.method.upper() == "POST":
        form = AddCustomTransactionToGroupForm(data=request.POST)
        val = form.is_valid()
        user_data = form.data
        transaction = user_data["transaction"]
        payer = user_data["payer"]
        details = user_data["details"]
        payee = form.cleaned_data["consumers"]

        grp = UserGroup.objects.get(id=usergroup_id)
        payer_user = User.objects.get(id=payer)
        payer_account = Account.objects.get(user_id=payer_user.id)
        num_of_users = payee.__len__()
        amount = float(transaction) / num_of_users

        for payee_s in payee:
            if payee_s != payer_user.username:
                user_account = User.objects.get(username=payee_s)
                account = Account.objects.get(user_id=user_account.id)
                Transaction.objects.create(name=details, payee=account,
                                           payer=payer_account,
                                           amount=amount, group=grp,                                               created=datetime.now())

            else:
                pass  # TODO

        return HttpResponseRedirect('/groups/' + str(usergroup_id))
    else:
        form = AddCustomTransactionToGroupForm()
        form.fields["payer"].queryset = User.objects.filter(groups__name=usergroup.group.name)
        payee_user = [str(payee_name) for payee_name in User.objects.filter(groups__name=usergroup.group.name)]
        form.fields["consumers"].choices = [(payee_name, payee_name) for payee_name in payee_user]
        return render(request, 'forms/add_custom_transaction.html',
                      {'form': form, 'usergroup_id': usergroup_id})


@login_required(login_url='/login')
def create_event_form(request, usergroup_id):
    """
    This view creates a form for adding a new Event.
    :param request: HttpRequest object
    :return: The group.html page if the event was successfully added, or the create_event_form.html page if not
    """
    try:
        usergroup = UserGroup.objects.get(id=usergroup_id)
    except UserGroup.DoesNotExist:
        usergroup = None  # TODO invalid usergroup_id

    if request.method.upper() == "POST":
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event_data = form.cleaned_data
            event_name = event_data["event_name"]

            # we generate unique name for django group by randomization
            unique_django_event_id = uuid.uuid4()

            while Event.objects.filter(id=unique_django_event_id).exists():
                unique_django_event_id = uuid.uuid4()

            Event.objects.create(name=event_name, id=unique_django_event_id, group=usergroup)

        else:
            pass  # TODO

        return HttpResponseRedirect('/groups/' + str(usergroup_id))
    else:
        return render(request, 'forms/create_event_form.html',
                      {'form': CreateEventForm(),
                       'usergroup_id': usergroup_id})


def delete_event(request, usergroup_id, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        event = None # TODO invalid event_id

    transactions = Transaction.objects.filter(event_id=event_id)
    for t in transactions:
        t.delete()
    event.delete()

    return HttpResponseRedirect('/groups/' + str(usergroup_id))

@login_required(login_url='/login')
def resolve_transactions(request, usergroup_id):
    """
        This view resolves the pending transactions. It is done by two ways, either optimising the number
        of transactions, or ensuring that every user has to make only at most one transaction.
        :param request: HttpRequest object
        :param usergroup_id: The unique UUID of the group.
        :return: The rendered page of the group if successful, and the resolve_group_expenses_form.html page if not.
        """
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
                #Adds to each user the money they owe/should receive in each transaction
                useramount_list[transaction.payee.user.username] -= transaction.amount
                useramount_list[transaction.payer.user.username] += transaction.amount
                #Marks the transactions as complete now (new transactions for resolutions will be made)
            updateTransactions = Transaction.objects.filter(group_id=usergroup_id).update(status='C')
            if resolution_type == "opt_tran":
                print('You have chosen to optimize overall transactions')
                sorted_transaction_list = sorted(useramount_list.items(), key=operator.itemgetter(1))
                optimize_by_transaction(sorted_transaction_list, usergroup)


            else:
                print('You have chosen to optimize per user')
                sorted_transaction_list = sorted(useramount_list.items(), key=operator.itemgetter(1))
                optimize_by_user(sorted_transaction_list, usergroup)
        else:
            #We do not need to worry about this use case as the form is just two radio buttons.
            pass #TODO

        return HttpResponseRedirect('/groups/' + str(usergroup_id))
    else:
        return render(request, 'forms/resolve_group_expenses_form.html',
                      {'form': ResolveTransactions(), 'usergroup_id': usergroup_id})


def optimize_by_transaction(sorted_transaction_list, usergroup):

    #The key is defined as the amount of money each user owes/is owed.
    def getKey(item):
        return item[1]

    #Sorts the list in ascending order (optimization method).
    sorted_transaction_list = sorted(sorted_transaction_list, key=getKey)

    #Identifies the first user, i.e, the user that owes the most amount of money
    first_key = sorted_transaction_list[0][0]
    first_value = sorted_transaction_list[0][1]
    firstTup = (first_key, first_value)
    first_value = first_value*-1

    #Identifies the last user, i.e, the user that is owed the most amount of money
    last_key = sorted_transaction_list[sorted_transaction_list.__len__()-1][0]
    last_value = sorted_transaction_list[sorted_transaction_list.__len__()-1][1]

    #Checks to see if all transactions are resolved
    if first_value == 0 and last_value == 0:
        return
    lastTup = (last_key, last_value)

    #Case: When the most owed user is owed less than the user who has to pay the most
    if first_value > last_value and sorted_transaction_list.__len__()>0:
        payee = User.objects.get(username=first_key)
        payer = User.objects.get(username=last_key)
        #Creates a transaction between the most owed and most indebted
        Transaction.objects.create(name='resolution', payee=Account.objects.get(user=payee),
                                       payer=Account.objects.get(user=payer),
                                       amount=last_value,
                                       group=usergroup,
                                       created=datetime.now())
        #Now that the most owed is not owed any more money, he/she can be removed from the list.
        sorted_transaction_list.remove(lastTup)
        sorted_transaction_list.remove(firstTup)
        #Update the value of the most in-debt.
        newTup = (first_key, last_value-first_value)
        sorted_transaction_list.append(newTup)
        optimize_by_transaction(sorted_transaction_list, usergroup)

    #Case: When the user who should get most amount of money cannot just be paid by the user who is in
    #maximum debt.
    else:
        payee = User.objects.get(username=first_key)
        payer = User.objects.get(username=last_key)
        Transaction.objects.create(name='resolution', payee=Account.objects.get(user=payee),
                                   payer=Account.objects.get(user=payer),
                                   amount=first_value,
                                   group=usergroup,
                                   created=datetime.now())
        #Remove the user who was in most debt (they have now paid up).
        sorted_transaction_list.remove(firstTup)
        sorted_transaction_list.remove(lastTup)
        newTup = (last_key, last_value-first_value)
        sorted_transaction_list.append(newTup)
        #Recursively run the code
        optimize_by_transaction(sorted_transaction_list, usergroup)

def optimize_by_user(sorted_transaction_list, usergroup):
    #The logic for this is similar to having all users stand in a circle, in order of how much they
    #are owed/owe. Every user who owes money pays to the person immediately to his/her right, and they collect
    #the money across the circle and when someone is owed money, they take their share and pass the rest of the
    #money along.
    amount = 0
    for i in range(sorted_transaction_list.__len__()-1):
        #first user is the one who is going to pay to the person on his/her right
        first_key = sorted_transaction_list[i][0]
        first_value = sorted_transaction_list[i][1]
        amount = amount + first_value
        #last user collects the value, then takes/add his/her share and passes it along.
        last_key = sorted_transaction_list[i+1][0]
        last_value = sorted_transaction_list[i+1][1]
        payee = User.objects.get(username=first_key)
        payer = User.objects.get(username=last_key)
        if amount<0:
            Transaction.objects.create(name='resolution', payee=Account.objects.get(user=payee),
                                       payer=Account.objects.get(user=payer),
                                       amount=amount*-1,
                                       group=usergroup,
                                       created=datetime.now())



