# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Account
from events.models import Event
from groups.models import UserGroup
from datetime import datetime
import uuid


class Transaction(models.Model):
    """
    The Transaction model represents a transaction between two Accounts in the same UserGroup.
    """
    # The name/label of the Transaction
    name = models.CharField(max_length=150)

    # A more detailed message about the Transaction provided by users
    message = models.TextField()

    # Unique UUID to distinguish Transactions with the same name/payer/payee
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # The Account who pays (payer) and the Account who receives (payee)
    payer = models.ForeignKey(Account, related_name='payer', on_delete=models.CASCADE, null=True)
    payee = models.ForeignKey(Account, related_name='payee', on_delete=models.CASCADE, null=True)

    # The amount of money involved in the Transaction
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # The currency in which the Transaction occurs
    CURRENCY_CHOICES = (
        ('EUR', 'Euro'),
        ('USD', 'US dollar'),
        ('PLN', 'Polish złoty'),
        ('INR', 'Indian rupee'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')

    # The UserGroup to which the Transaction belongs
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)

    # The Event to which the Transaction belongs
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    # The date/time that this transaction was created/finished
    created = models.DateTimeField(default=datetime.now)
    finished = models.DateTimeField(null=True)

    # The creator of the transaction
    creator = models.OneToOneField(Account, related_name='creator', on_delete=models.CASCADE, null=True)

    # The status of the transaction (opened/completed - maybe more in future)
    STATUS_CHOICES = (
        ('O', 'OPEN'),
        ('C', 'CLOSED'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='O')

    def __str__(self):
        """
        This function describes the relationship between payer and payee as a string.
        :return: A string representing the transaction
        """
        return '"' + self.name + '": ' + self.payer.user.username + ' pays ' + self.payee.user.username

    def is_open(self):
        """
        This function returns whether the transaction is currently pending.
        :return: A Boolean value
        """
        return self.status is 'O'

    def is_closed(self):
        """
        This function returns whether the transaction has been completed.
        :return: A Boolean value
        """
        return self.status is 'C'
