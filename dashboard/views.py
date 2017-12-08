# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models import Account
from transactions.models import Transaction
import requests
import json


def get_friends(account):
    """
    This function builds a list of the current user's friends.
    :param account: An instance of the Account model.
    :return: A list of Accounts that are friends with the provided Account.
    """
    subscribed_groups = account.user.groups.all()
    friends = []
    for grp in subscribed_groups:
        friends += [usr for usr in User.objects.filter(groups__name=grp.name) if
                    usr.account != account]
    friends = list(set(friends))  # remove duplicates
    return friends


@login_required(login_url='/login')
def dash(request):
    """
    This function builds a dashboard that is displayed as the current user's home page.
    It includes displays of how much money the user owes and is owed, which are combined into a total balance.
    It also displays the user's 10 most recent transactions.
    :param request: HttpRequest object
    :return: The rendered dashboard.html page.
    """

    r = requests.get('https://api.fixer.io/latest')
    rates = json.loads(r.text)
    print(rates['base'])

    my_account = Account.objects.get(user=request.user)
    groups = request.user.groups.all()

    # A user's "friends" are the other members of the groups that he/she is in.
    # We may add a more reciprocal system for friends (like FB) in the future.
    friends = get_friends(my_account)

    amount_due = 0.0
    amount_owed = 0.0

    expenses_due = Transaction.objects.filter(payer=my_account)
    for t in expenses_due:
        if t.status == 'O':
            amount_due += float(t.expense.amount)

    expenses_owed = Transaction.objects.filter(payee=my_account)
    for t in expenses_owed:
        if t.status == 'O':
            amount_owed += float(t.expense.amount)

    balance = amount_due - amount_owed

    transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    transactions = transactions.order_by('-created')[:10]

    amount_owed_string = "-€%.2f" % abs(amount_owed) if (balance < 0) else "€%.2f" % abs(amount_owed)
    balance_string = "-€%.2f" % abs(balance) if (balance < 0) else "€%.2f" % abs(balance)

    return render(request, 'sites/dashboard.html',
                  {'my_account': my_account, 'n_groups': groups.count(),
                   'n_friends': len(friends),
                   'amount_due': amount_due,
                   'amount_due_string': "€%.2f" % amount_due,
                   'amount_owed': amount_owed,
                   'amount_owed_string': amount_owed_string,
                   'balance': balance,
                   'balance_string': balance_string,
                   'transactions': transactions})
