from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models import Account
from transactions.models import Transaction


def get_friends(account):
    subscribed_groups = account.user.groups.all()
    friends = []
    for grp in subscribed_groups:
        friends += [usr for usr in User.objects.filter(groups__name=grp.name) if
                    usr.account != account]
    friends = list(set(friends))  # remove duplicates
    return friends


@login_required(login_url='/login')
def dash(request):
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
            amount_due += float(t.amount)

    expenses_owed = Transaction.objects.filter(payee=my_account)
    for t in expenses_owed:
        if t.status == 'O':
            amount_owed += float(t.amount)

    balance = amount_due - amount_owed

    transactions = Transaction.objects.filter(
        payee=my_account) | Transaction.objects.filter(payer=my_account)
    transactions = transactions.order_by('-created')[:10]

    return render(request, 'sites/dashboard.html',
                  {'my_account': my_account, 'n_groups': groups.count(),
                   'n_friends': len(friends),
                   'amount_due': amount_due,
                   'amount_due_string': "€%.2f" % amount_due,
                   'amount_owed': amount_owed,
                   'amount_owed_string': "€%.2f" % amount_owed,
                   'balance': balance,
                   'balance_string': "€%.2f" % abs(balance),
                   'transactions': transactions})
