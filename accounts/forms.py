# -*- coding: utf-8 -*-

from django import forms


class UserRegistrationForm(forms.Form):
    """
    This is the form for registering a new user in the application.
    """
    username = forms.CharField(
        required=True,
        label='username',
        max_length=32
    )
    first_name = forms.CharField(
        required=True,
        label='first_name',
        max_length=50
    )
    last_name = forms.CharField(
        required=True,
        label='last_name',
        max_length=50
    )
    email = forms.CharField(
        required=True,
        label='email',
        max_length=32,
    )
    password = forms.CharField(
        required=True,
        label='password',
        max_length=32,
        widget=forms.PasswordInput()
    )


class UserSettingsForm(forms.Form):
    """
    This is the form for changing the user's settings.
    """
    CURRENCY_CHOICES = (
        ('EUR', 'Euro'),
        ('USD', 'US dollar'),
        ('PLN', 'Polish złoty'),
        ('INR', 'Indian rupee'),
    )

    currency = forms.ChoiceField(widget=forms.Select, choices=CURRENCY_CHOICES)