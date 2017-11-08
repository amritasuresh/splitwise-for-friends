from django import forms

# Leaving these blank since this functionality is just accessed through buttons for now.


class ResolveBalanceForm(forms.Form):
    """
    This form is used to resolve outstanding balances between users.
    """
    pass


class PayTransactionForm(forms.Form):
    """
    This form is used to pay and complete a transaction.
    """
    pass


class DeleteTransactionForm(forms.Form):
    """
    This form is used to delete a transaction.
    """
    pass