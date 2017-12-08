from django import forms

#This form creates a group with the input of the group name

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=80, empty_value=False)

# This form adds a user to a given group

class AddUserToGroupForm(forms.Form):
    username = forms.CharField(max_length=80, empty_value=False)

#This form adds a transaction (payment) to the group. Currently, one payment is divided equally among
#all members of the group. Future functionality may include choosing members to split the amount

class AddTransactionToGroupForm(forms.Form):
    transaction = forms.CharField(max_length=80, empty_value=False)
    payer = forms.CharField(max_length=80, empty_value=False)
    details = forms.CharField(max_length=80, empty_value=False)


class ResolveTransactions(forms.Form):
    resolutiontype = forms.RadioSelect()