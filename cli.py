from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from datetime import datetime
import uuid
from django.contrib.auth.models import Group

from accounts.models import Account
from transactions.models import Transaction
from groups.models import UserGroup

# A basic command line interface that lets you create a user, add a transaction, view transactions, create group
# This tool does not settle the dues like the web interface, we can add that as a later part of the project.
# Also, basic tests like redundancy and false values need to be checked.

def create_user(username, firstname, lastname, password, email):
    """
    This function creates a user.
    :param username: The user's username
    :param firstname: The user's first name
    :param lastname: The user's last name
    :param password: The user's password
    :param email: The user's email
    :return:
    """
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
    """
    This function creates a transaction within a given group by prompting the user information.
    :return:
    """
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
    """
    This function is a placeholder for the user creation to get the details from the command line.
    :return:
    """
    username = input("Enter user name\n")
    password = input("Enter password\n")
    firstname = input("Enter first name\n")
    lastname= input("Enter last name\n")
    email = input("Enter email\n")
    create_user(username, firstname, lastname, password, email)


def view_transactions():
    """
    This function allows the user to view transactions from the database.
    :return:
    """
    groupname = input("Enter group name")
    grp = UserGroup.objects.get(group_name=groupname)
    print(Transaction.objects.filter(group=grp))


def view_balance():
    """
    This function displays the list of all transactions for a given user (the money that the user is owed).
    :return:
    """
    username = input("Enter user name")
    payeruser = User.objects.get(username=username)
    payeracc = Account.objects.get(user_id=payeruser.id)
    print(Transaction.objects.filter(payer=payeracc))


def add_user_to_group():
    """
    This function adds an existing user to an existing group.
    :return:
    """
    groupname = input("Enter the group you want to add user to")
    username = input("Enter user name to be added to the group")
    grp = UserGroup.objects.get(group_name=groupname)
    user = User.objects.get(username=username)
    user.groups.add(grp)


def create_new_group():
    """
    This function creates a new group.
    :return:
    """
    groupname = input("Enter group name")
    unique_django_group_id = uuid.uuid4()

    while Group.objects.filter(name=unique_django_group_id).exists():
        unique_django_group_id = uuid.uuid4()

    grp = Group.objects.create(name=unique_django_group_id)

    UserGroup.objects.create(group=grp, group_name=groupname,
                             created=datetime.now())

# Basic tool to add the details

act = input("Hello, pick a choice between the following actions: 1. Create new user\n 2. Add transaction\n 3. View transactions\n 4. View balance\n 5. Add user to group\n 6. Create new group\n")
if act == '1':
    create()
elif act == '2':
    add_transaction()
elif act == '3':
    view_transactions()
elif act == '4':
    view_balance()
elif act == '5':
    add_user_to_group()
elif act == '6':
    create_new_group()






