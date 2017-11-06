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

    can_pay = False
    my_account = Account.objects.get(user=request.user)
    if my_account == t.payee:
            can_pay = True

    if t.status != 'C' and can_pay:
        t.status = 'C'
        t.finished = datetime.now()

    t.save()

    return render(request, 'sites/transaction_payment.html',
                  {'my_account': my_account, 'transaction': t,
                   'transaction_amount': "€%.2f" % t.amount,
                   'can_pay': can_pay})


@login_required(login_url='/login')
def delete(request, transaction_id):
    try:
        t = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        t = None  # TODO invalid transaction id

    can_delete = False
    my_account = Account.objects.get(user=request.user)
    if my_account == t.payee or my_account == t.payer:
            can_delete = True

    print(can_delete)
    name = t.name
    print(name)
    print(t.status)
    if t.status != 'C' and can_delete:
        t.delete()

    return render(request, 'sites/transaction_deletion.html',
                  {'my_account': my_account, 'transaction_name': name,
                   'can_delete': can_delete})
