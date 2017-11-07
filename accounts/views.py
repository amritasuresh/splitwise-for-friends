from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms

from accounts.models import Account
import dashboard.views
from .forms import UserRegistrationForm

def home(request):
    """
    This is the view for the homepage.
    :param request: HttpRequest object
    :return: Either the user's dashboard if the user is logged in, or the login page if not.
    """
    if request.user.is_authenticated():
        return dashboard.views.dash(request)
    else:
        return HttpResponseRedirect('/login')


def register(request):
    """
    This is the view used for registering new users.
    :param request: HttpRequest object
    :return: The rendered register.html page.
    """
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
    """
    This page is where users are redirected if they forget their passwords.
    :param request: HttpRequest object
    :return: The rendered forgotpassword.html page.
    """
    # TODO FORGOT PASSWORD PAGE
    return render(request, 'sites/forgotpassword.html')

#This is the view where all users are displayed

@login_required(login_url='/login')
def users(request):
    """
    This view displays all users of the application.
    :param request: HttpRequest object
    :return: The rendered users.html page.
    """
    all_users = User.objects.all()
    my_account = Account.objects.get(user=request.user)
    return render(request, 'sites/users.html', {'users': all_users,
                                                'my_account': my_account})


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
def friends(request):
    """
    This page displays all of the current user's friends.
    :param request: HttpRequest object
    :return: The rendered friends.html page.
    """
    my_account = Account.objects.get(user=request.user)
    my_friends = get_friends(my_account)
    return render(request, 'sites/friends.html', {'users': my_friends,
                                                'my_account': my_account})


@login_required(login_url='/login')
def profile_page(request):
    """
    This page displays the current user's profile upon logging in.
    :param request: HttpRequest object
    :return: The rendered profilepage.html page.
    """
    my_account = Account.objects.get(user=request.user)
    friends = get_friends(my_account)
    return render(request, 'sites/profilepage.html', {'my_account': my_account,
                                                      'friends': friends})

#User page

@login_required(login_url='/login')
def user_page(request, user_id):
    """
    This page displays the profile of the given user.
    :param request: HttpRequest object
    :param user_id: An integer that serves to uniquely distinguish the given user.
    :return: The rendered user.html page.
    """
    my_account = Account.objects.get(user=request.user)
    target_account = Account.objects.get(user_id=user_id)
    friends = get_friends(target_account)
    return render(request, 'sites/user.html', {'my_account': my_account,
                                               'target_account': target_account,
                                               'friends': friends})