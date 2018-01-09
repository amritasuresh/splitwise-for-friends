from django import forms
from accounts.models import Account
from django.contrib.auth.models import User
#This form creates a group with the input of the group name

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=80, empty_value=False)

# This form adds a user to a given group

class AddUserToGroupForm(forms.Form):
    username = forms.ModelChoiceField(queryset=Account.objects.all())

#This form adds a transaction (payment) to the group. Currently, one payment is divided equally among
#all members of the group. Future functionality may include choosing members to split the amount

class AddTransactionToGroupForm(forms.Form):
    transaction = forms.CharField(max_length=80, empty_value=False)
    payer = forms.ModelChoiceField(queryset=User.objects.none())
    details = forms.CharField(max_length=80, empty_value=False)


class ResolveTransactions(forms.Form):
    resolutiontype = forms.RadioSelect()

class AddCustomTransactionToGroupForm(forms.Form):
    transaction = forms.CharField(max_length=80, empty_value=False)
    payee_user = [str(payee_name) for payee_name in User.objects.all()]
    payee = forms.MultipleChoiceField(choices=([(payee_name, payee_name) for payee_name in payee_user]), widget=forms.CheckboxSelectMultiple(), required=True)
    #payee = forms.MultipleChoiceField(queryset=User.objects.none(), widget=forms.CheckboxSelectMultiple(), required=True)
    payer = forms.ModelChoiceField(queryset=User.objects.none(), required=True)
    #payee = forms.MultipleChoiceField(choices=user_list, widget=forms.CheckboxSelectMultiple())
    details = forms.CharField(max_length=80, empty_value=False)
    def clean_recipients(self):
        data = self.cleaned_data['payee']
        if data == "select":
            raise forms.ValidationError("Select account type.")
        return data