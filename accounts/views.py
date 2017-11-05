from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms

from accounts.models import Account
from .forms import UserRegistrationForm


def home(request):
    if request.user.is_authenticated():
        return profile_page(request)
    else:
        return HttpResponseRedirect('/login')


def register(request):
    if request.method.upper() == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            username = user_data['username']
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            email = user_data['email']
            password = user_data['password']
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
                                         first_name=first_name,
                                         last_name=last_name)

                user = authenticate(username=username, password=password)
                Account.objects.create(user=user)
                login(request, user)

                # TODO: Sending emails with registration data
                return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'sites/register.html', {'form': form})


def forgot_password(request):
    # TODO FORGOT PASSWORD PAGE
    return render(request, 'sites/forgotpassword.html')


@login_required(login_url='/login')
def users(request):
    all_users = User.objects.all()
    my_account = Account.objects.get(user=request.user)
    return render(request, 'sites/users.html', {'users': all_users,
                                                'my_account': my_account})


def get_friends(account):
    subscribed_groups = account.user.groups.all()
    friends = []
    for grp in subscribed_groups:
        friends += [usr for usr in User.objects.filter(groups__name=grp.name) if
                    usr.account != account]
    friends = list(set(friends))  # remove duplicates
    return friends


@login_required(login_url='/login')
def profile_page(request):
    my_account = Account.objects.get(user=request.user)
    friends = get_friends(my_account)
    return render(request, 'sites/profilepage.html', {'my_account': my_account,
                                                      'friends': friends})


@login_required(login_url='/login')
def user_page(request, user_id):
    my_account = Account.objects.get(user=request.user)
    target_account = Account.objects.get(user_id=user_id)
    friends = get_friends(target_account)
    return render(request, 'sites/user.html', {'my_account': my_account,
                                               'target_account': target_account,
                                               'friends': friends})