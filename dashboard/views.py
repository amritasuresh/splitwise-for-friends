# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models import Account
from transactions.models import Transaction

import requests, json, decimal


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

    # In order to convert between currencies, we need to get the latest exchange rates.
    # We use the Fixer API to get the daily exchange rates from the European Central Bank: http://fixer.io/
    #
    # If the transactions are not already in the user's chosen currency, we first convert from the transaction's
    # currency into euros, and then from euros into the user's currency.
    r = requests.get('https://api.fixer.io/latest')
    text = json.loads(r.text)
    rates = text["rates"]

    expenses_due = Transaction.objects.filter(payer=my_account)
    for t in expenses_due:
        if t.status == 'O':
            amount = t.amount
            currency = t.currency
            if(currency != 'EUR'):
                rate = rates[currency]
                amount *= 1.0/rate
            amount_due += float(amount)

    expenses_owed = Transaction.objects.filter(payee=my_account)
    for t in expenses_owed:
        if t.status == 'O':
            amount = t.amount
            currency = t.currency
            if (currency != 'EUR'):
                rate = rates[currency]
                amount *= 1.0 / rate
            amount_owed += float(amount)

    amount_due = float(format(amount_due, '.2f'))
    amount_owed = float(format(amount_owed, '.2f'))

    balance = amount_due - amount_owed
    if(my_account.currency != 'EUR'):
        rate = rates[my_account.currency]
        balance *= rate
        amount_due *= rate
        amount_owed *= rate

    transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    transactions = transactions.order_by('-created')[:10]

    for t in transactions:
        if t.currency != my_account.currency:
            if t.currency != 'EUR':
                rate = rates[t.currency]
                t.amount *= 1.0 / rate
            rate = rates[my_account.currency]
            t.amount *= decimal.Decimal(rate)
        t.amount = float(format(t.amount, '.2f'))

    symbols = {'EUR': '€', 'USD': '$', 'PLN': ' zł', 'INR': '₹ '}
    symbol = symbols.get(my_account.currency, 'default')
    if(my_account.currency == 'PLN'):
        amount_due_string = ("%.2f " % amount_due) + symbol
        amount_owed_string = (("-%.2f" % abs(amount_owed)) + symbol) if (balance < 0) else ("%.2f" % abs(amount_owed)) + symbol
        balance_string = (("-%.2f" % abs(balance)) + symbol) if (balance < 0) else ("%.2f" % abs(balance)) + symbol
    else:
        amount_due_string = symbol + ("%.2f" % amount_due)
        amount_owed_string = "-" + symbol + ("%.2f" % abs(amount_owed)) if (balance < 0) else symbol + ("%.2f" % abs(amount_owed))
        balance_string = "-" + symbol + ("%.2f" % abs(balance)) if (balance < 0) else symbol + ("%.2f" % abs(balance))

    transaction_strings = []
    for t in transactions:
        if(my_account.currency == 'PLN'):
            s = ("%.2f " % t.amount) + symbol
        else:
            s = symbol + ("%.2f" % t.amount)

        transaction_strings.append(s)

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
