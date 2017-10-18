from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
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
            email = user_data['email']
            password = user_data['password']
            user_exists = User.objects.filter(username=username).exists()
            email_exists = User.objects.filter(email=email).exists()

            if user_exists or email_exists:
                # TODO: Generate some error message and redict to error page
                raise forms.ValidationError(
                    'Looks like a username with that email '
                    'or password already exists')
            else:
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                # TODO: Sending emails with registration data
                # TODO: redict to home page
                return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'sites/register.html', {'form': form})


def forgot_password(request):
    # TODO FORGOT PASSWORD PAGE
    return render(request, 'sites/forgotpassword.html')


def users(request):
    return render(request, 'sites/users.html')


def profile_page(request):
    return render(request, 'sites/profilepage.html')