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
