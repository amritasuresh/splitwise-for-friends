from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from datetime import datetime

from accounts.models import Account
from transactions.models import Transaction
from groups.models import UserGroup

def create_user(username, firstname, lastname, password, email):
    user_exists = User.objects.filter(username=username).exists()
    email_exists = User.objects.filter(email=email).exists()

    if user_exists or email_exists:
        # TODO: Generate some error message and redict to error page
        raise forms.ValidationError(
            'Looks like a username with that email ' +
            'or password already exists')
    else:
        User.objects.create_user(username=username, email=email,
                                 password=password,
                                 first_name=firstname,
                                 last_name=lastname)

        user = authenticate(username=username, password=password)
        Account.objects.create(user=user)

def add_transaction():
    amount = input("Enter amount\n")
    payer = input("Enter payer username\n")
    group = input("Enter group name\n")
    details = input("Enter details\n")

    payeruser = User.objects.get(username=payer)
    payeracc = Account.objects.get(user_id=payeruser.id)

    grp = UserGroup.objects.get(group_name=group)
    users = User.objects.filter(groups__name=grp.group.name)

    for user in users:
        if user.id != payeruser.id:
            useracc = User.objects.get(username=user)
            acc = Account.objects.get(user_id=useracc.id)
            Transaction.objects.create(name=details, payee=acc, payer=payeracc, amount=amount, group=grp)

def create():
    username = input("Enter user name\n")
    password = input("Enter password\n")
    firstname = input("Enter first name\n")
    lastname= input("Enter last name\n")
    email = input("Enter email\n")
    create_user(username, firstname, lastname, password, email)

def view_transactions():
    groupname = input("Enter group name")
    grp = UserGroup.objects.get(group_name=groupname)
    print(Transaction.objects.filter(group=grp))

def view_balance():
    username = input("Enter user name")
    payeruser = User.objects.get(username=username)
    payeracc = Account.objects.get(user_id=payeruser.id)
    print(Transaction.objects.filter(payer=payeracc))


from accounts.forms import UserRegistrationForm
act = input("Hello, pick a choice between the following actions: 1. Create new user 2. Add transaction 3. View transactions 4. View balance\n")
if act == '1':
    create()
elif act == '2':
    add_transaction()
elif act == '3':
    view_transactions()
elif act == '4':
    view_balance()







