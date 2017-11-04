from django import forms


class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=80, empty_value=False)


class AddUserToGroupForm(forms.Form):
    username = forms.CharField(max_length=80, empty_value=False)

class AddTransactionToGroupForm(forms.Form):
    transaction = forms.CharField(max_length=80, empty_value=False)
    payer = forms.CharField(max_length=80, empty_value=False)
    details = forms.CharField(max_length=80, empty_value=False)


