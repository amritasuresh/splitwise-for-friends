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

# Create your views here.


@login_required(login_url='/login')
def transactions(request):
    my_account = Account.objects.get(user=request.user)
    my_transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    my_transactions = my_transactions.order_by('-created')
    transactions_due = Transaction.objects.filter(payer=my_account).order_by('-created')
    transactions_owed = Transaction.objects.filter(payee=my_account).order_by('-created')

    return render(request, 'sites/transactions.html',
                  {'my_account': my_account,
                   'transactions': my_transactions,
                   'transactions_due': transactions_due,
                   'transactions_owed': transactions_owed,
                   'pending': False,
                   'completed': False})


@login_required(login_url='/login')
def pending(request):
    my_account = Account.objects.get(user=request.user)
    my_transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    my_transactions = my_transactions.filter(status='O').order_by('-created')
    transactions_due = my_transactions.filter(payer=my_account).order_by('-created')
    transactions_owed = my_transactions.filter(payee=my_account).order_by('-created')

    return render(request, 'sites/transactions.html',
                  {'my_account': my_account,
                   'transactions': my_transactions,
                   'transactions_due': transactions_due,
                   'transactions_owed': transactions_owed,
                   'pending': True,
                   'completed': False})

@login_required(login_url='/login')
def completed(request):
    my_account = Account.objects.get(user=request.user)
    my_transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    my_transactions = my_transactions.filter(status='C').order_by('-created')
    transactions_due = my_transactions.filter(payer=my_account).order_by('-created')
    transactions_owed = my_transactions.filter(payee=my_account).order_by('-created')

    return render(request, 'sites/transactions.html',
                  {'my_account': my_account,
                   'transactions': my_transactions,
                   'transactions_due': transactions_due,
                   'transactions_owed': transactions_owed,
                   'pending': False,
                   'completed': True})


@login_required(login_url='/login')
def transaction(request, transaction_id):
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

    return render(request, 'sites/transaction.html',
                  {'my_account': my_account, 'transaction': t,
                   'transaction_amount': "€%.2f" % t.amount,
                   'date_created': t.created.strftime("%d/%m/%Y"),
                   'completed': t.status == 'C',
                   'can_pay': can_pay,
                   'can_edit': can_edit,
                   'can_delete': can_delete})


@login_required(login_url='/login')
def pay(request, transaction_id):
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
    print("greetings")
    my_account = Account.objects.get(user=request.user)
    friends = get_friends(my_account)

    resolution_list = []
    for friend in friends:
        transactions_due = Transaction.objects.filter(Q(payee=friend.account) & Q(payer=my_account))
        amount_due = 0.0
        for t in transactions_due:
            if t.status != 'C':
                amount_due += float(t.amount)

        transactions_owed = Transaction.objects.filter(Q(payer=friend.account) & Q(payee=my_account))
        amount_owed = 0.0
        for t in transactions_owed:
            if t.status != 'C':
                amount_owed += float(t.amount)

        balance = amount_due - amount_owed
        if balance != 0:
            balance_str = "€%.2f" % abs(balance)
            resolution_list.append([friend, balance, balance_str])

    return render(request, 'sites/resolution.html',
                  {'my_account': my_account, 'resolution_list': resolution_list})


@login_required(login_url='/login')
def resolve_balance(request, user_id):
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
