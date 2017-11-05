from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User

from accounts.models import Account
from transactions.models import Transaction

# Create your views here.


@login_required(login_url='/login')
def dash(request):
    account = Account.objects.get(user=request.user)
    groups = request.user.groups.all()

    # A user's "friends" are the other members of the groups that he/she is in.
    # We may add a more reciprocal system for friends (like Facebook) in the future.
    friends = set()

    expenses_received = 0.0
    expenses_paid = 0.0
    for g in groups:
        users = User.objects.filter(groups__name=g.name)
        for u in users:
            print(u)
            friends.add(u)

    transactions_received = Transaction.objects.filter(payee=account)
    for t in transactions_received:
        if t.status == 'O':
            expenses_received += float(t.amount)

    transactions_paid = Transaction.objects.filter(payer=account)
    for t in transactions_paid:
        if t.status == 'C':
            expenses_paid += float(t.amount)

    if request.user in friends:
        friends.remove(request.user)

    transactions = Transaction.objects.filter(payee=account) | Transaction.objects.filter(payer=account)
    transactions.order_by('-created')[:5]

    return render(request, 'sites/dashboard.html', {'account': account, 'n_groups': groups.count(),
                                                    'n_friends': len(friends),
                                                    'expenses_received': "%.2f" % expenses_received,
                                                    'expenses_paid': "%.2f" % expenses_paid,
                                                    'transactions': transactions})