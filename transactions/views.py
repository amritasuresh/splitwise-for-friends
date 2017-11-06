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
    my_transactions = my_transactions.order_by('-created')[:10]
    transactions_due = Transaction.objects.filter(payer=my_account).order_by('-created')
    transactions_owed = Transaction.objects.filter(payee=my_account).order_by('-created')

    return render(request, 'sites/transactions.html',
                  {'my_account': my_account,
                   'transactions': my_transactions,
                   'transactions_due': transactions_due,
                   'transactions_owed': transactions_owed})
