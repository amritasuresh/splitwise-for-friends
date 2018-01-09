# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from accounts.models import Account
from transactions.models import Transaction
from transactions.forms import ResolveBalanceForm, PayTransactionForm, DeleteTransactionForm
from dashboard.views import get_friends

from currencies.views import get_exchange_rates, get_symbol, convert_amount, amount_as_string

import decimal

# Create your views here.


@login_required(login_url='/login')
def convert_transactions(request, my_transactions, transactions_due, transactions_owed, my_account):
    """
    This function converts all transactions to the user's choice of currency and associates a string with each
    transaction (e.g. "€100.00")
    :param request: HttpRequest object
    :param my_transactions: list of all transactions
    :param transactions_due: list of transactions containing outstanding payments for the user
    :param transactions_owed: list of transactions containing outstanding payments the user must pay
    :param my_account: the user's Account
    :return: list1, list2, list3: zipped lists associating each transaction with a string, for use in transactions.html
    """
    for t in my_transactions:
        amount = convert_amount(request, t.amount, t.currency, my_account.currency)
        t.amount = float(format(amount, '.2f'))

    for t in transactions_due:
        amount = convert_amount(request, t.amount, t.currency, my_account.currency)
        t.amount = float(format(amount, '.2f'))

    for t in transactions_owed:
        amount = convert_amount(request, t.amount, t.currency, my_account.currency)
        t.amount = float(format(amount, '.2f'))

    transaction_strings = []
    transactions_due_strings = []
    transactions_owed_strings = []

    for t in my_transactions:
        transaction_strings.append(amount_as_string(request, t.amount, my_account))

    for t in transactions_due:
        transactions_due_strings.append(amount_as_string(request, t.amount, my_account))

    for t in transactions_owed:
        transactions_owed_strings.append(amount_as_string(request, t.amount, my_account))

    list1 = zip(my_transactions, transaction_strings)
    list2 = zip(transactions_due, transactions_due_strings)
    list3 = zip(transactions_owed, transactions_owed_strings)

    return list1, list2, list3


@login_required(login_url='/login')
def transactions(request):
    """
    This function renders a page displaying all transactions that the user is involved in.
    :param request: HttpRequest object
    :return: The rendered transactions.html page.
    """
    my_account = Account.objects.get(user=request.user)
    my_transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    my_transactions = my_transactions.order_by('-created')
    transactions_due = Transaction.objects.filter(payer=my_account).order_by('-created')
    transactions_owed = Transaction.objects.filter(payee=my_account).order_by('-created')

    list1, list2, list3 = convert_transactions(request, my_transactions, transactions_due, transactions_owed, my_account)

    return render(request, 'sites/transactions.html',
                  {'my_account': my_account,
                   'transactions': list1,
                   'transactions_due': list2,
                   'transactions_owed': list3,
                   'pending': False,
                   'completed': False})


@login_required(login_url='/login')
def pending(request):
    """
    This function renders a page displaying only those transactions that are not yet resolved.
    :param request: HttpRequest object
    :return: The rendered transactions.html page.
    """
    my_account = Account.objects.get(user=request.user)
    my_transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    my_transactions = my_transactions.filter(status='O').order_by('-created')
    transactions_due = my_transactions.filter(payer=my_account).order_by('-created')
    transactions_owed = my_transactions.filter(payee=my_account).order_by('-created')

    list1, list2, list3 = convert_transactions(request, my_transactions, transactions_due, transactions_owed, my_account)

    return render(request, 'sites/transactions.html',
                  {'my_account': my_account,
                   'transactions': list1,
                   'transactions_due': list2,
                   'transactions_owed': list3,
                   'pending': True,
                   'completed': False})


@login_required(login_url='/login')
def completed(request):
    """
    This function renders a page displaying only those transactions that have already been completed.
    :param request: HttpRequest object
    :return: The rendered transactions.html page.
    """
    my_account = Account.objects.get(user=request.user)
    my_transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    my_transactions = my_transactions.filter(status='C').order_by('-created')
    transactions_due = my_transactions.filter(payer=my_account).order_by('-created')
    transactions_owed = my_transactions.filter(payee=my_account).order_by('-created')

    list1, list2, list3 = convert_transactions(request, my_transactions, transactions_due, transactions_owed, my_account)

    return render(request, 'sites/transactions.html',
                  {'my_account': my_account,
                   'transactions': list1,
                   'transactions_due': list2,
                   'transactions_owed': list3,
                   'pending': False,
                   'completed': True})


@login_required(login_url='/login')
def transaction(request, transaction_id):
    """
    This function renders a page displaying an individual transaction, and potentially allows the user to pay, edit,
    or delete the transaction depending on their permissions.
    :param request: HttpRequest object
    :param transaction_id: The UUID of the given transaction.
    :return:
    """
    try:
        t = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        t = None  # TODO invalid transaction id

    can_pay = False
    can_edit = False
    can_delete = False
    my_account = Account.objects.get(user=request.user)

    if my_account == t.payer or my_account == t.payee:
        can_edit = True
        can_delete = True
        if my_account == t.payee:
            can_pay = True

    amount = convert_amount(request, t.amount, t.currency, my_account.currency)
    string = amount_as_string(request, amount, my_account)

    return render(request, 'sites/transaction.html',
                  {'my_account': my_account, 'transaction': t,
                   'transaction_amount': string,
                   'date_created': t.created.strftime("%d/%m/%Y"),
                   'completed': t.status == 'C',
                   'can_pay': can_pay,
                   'can_edit': can_edit,
                   'can_delete': can_delete})


@login_required(login_url='/login')
def pay(request, transaction_id):
    """
    This function is called when the user attempts to pay an individual transaction. If it is successful, the
    transaction is set to completed within the database.
    :param request: HttpRequest object
    :param transaction_id: The UUID of the given transaction.
    :return:
    """
    try:
        t = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        t = None  # TODO invalid transaction id

    if request.method.upper() == "POST":
        form = PayTransactionForm(request.POST)
        if form.is_valid() and t.status != 'C':
            t.status = 'C'
            t.finished = datetime.now()
            t.save()
        else:
            pass
    else:
        pass

    return HttpResponseRedirect('/transactions/' + str(transaction_id) + '/')


@login_required(login_url='/login')
def delete(request, transaction_id):
    """
    This function is called when the user attempts to delete an individual transaction. If it is successful, the
    transaction is removed from the database.
    :param request: HttpRequest object
    :param transaction_id: The UUID of the given transaction.
    :return:
    """
    try:
        t = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        t = None  # TODO invalid transaction id

    print(request.method.upper())
    if request.method.upper() == "POST":
        form = DeleteTransactionForm(request.POST)
        print(t.status)
        if form.is_valid() and t.status != 'C':
            t.delete()
        else:
            pass
    else:
        pass

    return HttpResponseRedirect('/transactions/')


@login_required(login_url='/login')
def resolution(request):
    """
    This function renders a page displaying all of the potential resolutions for the current user, and allows them
    to resolve any negative balances that they owe to their friends.
    :param request: HttpRequest object
    :return: The rendered resolution.html page.
    """
    my_account = Account.objects.get(user=request.user)
    friends = get_friends(my_account)

    resolution_list = []
    for friend in friends:
        transactions_due = Transaction.objects.filter(Q(payee=friend.account) & Q(payer=my_account))
        amount_due = 0.0
        for t in transactions_due:
            if t.status != 'C':
                amount_due += float(t.amount)
        amount_due = convert_amount(request, decimal.Decimal(amount_due), t.currency, my_account.currency)

        transactions_owed = Transaction.objects.filter(Q(payer=friend.account) & Q(payee=my_account))
        amount_owed = 0.0
        for t in transactions_owed:
            if t.status != 'C':
                amount_owed += float(t.amount)
        amount_owed = convert_amount(request, decimal.Decimal(amount_owed), t.currency, my_account.currency)

        balance = amount_due - amount_owed
        if balance != 0:
            balance_str = amount_as_string(request, abs(balance), my_account)
            resolution_list.append([friend, balance, balance_str])

    return render(request, 'sites/resolution.html',
                  {'my_account': my_account, 'resolution_list': resolution_list})


@login_required(login_url='/login')
def resolve_balance(request, user_id):
    """
    This function allows the current user to instantly resolve a negative balance that is owed to another user.
    :param request: HttpRequest object
    :param user_id: The other user's unique ID.
    :return: The rendered page of resolutions.
    """
    my_account = Account.objects.get(user=request.user)
    try:
        friend_account = Account.objects.get(user_id=user_id)
    except Account.DoesNotExist:
        friend_account = None

    # Mark all the transactions between my friend and me as completed.
    if request.method.upper() == "POST":
        form = ResolveBalanceForm(request.POST)
        if form.is_valid():
            ts = Transaction.objects.filter(Q(payee=friend_account) & Q(payer=my_account))\
                       | Transaction.objects.filter(Q(payer=friend_account) & Q(payee=my_account))
            for t in ts:
                t.status = 'C'
                t.save()
        else:
            pass
    else:
        pass

    return HttpResponseRedirect('/transactions/resolution/')
