# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models import Account
from transactions.models import Transaction

from currencies.views import get_symbol, get_exchange_rates, convert_amount, amount_as_string

import decimal


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
    my_account = Account.objects.get(user=request.user)
    groups = request.user.groups.all()

    # A user's "friends" are the other members of the groups that he/she is in.
    # We may add a more reciprocal system for friends (like FB) in the future.
    friends = get_friends(my_account)

    amount_due = 0.0
    amount_owed = 0.0

    rates = get_exchange_rates(request)

    # If the transactions are not already in the user's chosen currency, we first convert from the transaction's
    # currency into euros, and then from euros into the user's currency.
    expenses_due = Transaction.objects.filter(payer=my_account, status='O')
    for t in expenses_due:
        amount = convert_amount(request, t.amount, t.currency, my_account.currency)
        amount_due += float(amount)
    amount_due = float(format(amount_due, '.2f'))

    expenses_owed = Transaction.objects.filter(payee=my_account, status='O')
    for t in expenses_owed:
        amount = convert_amount(request, t.amount, t.currency, my_account.currency)
        amount_owed += float(amount)
    amount_owed = float(format(amount_owed, '.2f'))

    balance = amount_due - amount_owed

    transactions = Transaction.objects.filter( payee=my_account) | Transaction.objects.filter(payer=my_account)
    transactions = transactions.order_by('-created')[:10]

    for t in transactions:
        amount = convert_amount(request, t.amount, t.currency, my_account.currency)
        t.amount = float(format(amount, '.2f'))

    amount_due_string = amount_as_string(request, amount_due, my_account)
    amount_owed_string = amount_as_string(request, amount_owed, my_account)
    balance_string = amount_as_string(request, balance, my_account)

    transaction_strings = []
    for t in transactions:
        transaction_strings.append(amount_as_string(request, t.amount, my_account))

    list = zip(transactions, transaction_strings)

    return render(request, 'sites/dashboard.html',
                  {'my_account': my_account, 'n_groups': groups.count(),
                   'n_friends': len(friends),
                   'amount_due': amount_due,
                   'amount_due_string': amount_due_string,
                   'amount_owed': amount_owed,
                   'amount_owed_string': amount_owed_string,
                   'balance': balance,
                   'balance_string': balance_string,
                   'transactions': list})
