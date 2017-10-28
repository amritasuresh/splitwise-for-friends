# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Account
from groups.models import UserGroup
from datetime import datetime
import uuid


# The Transaction model represents a transaction between two Accounts in the same UserGroup
class Transaction(models.Model):
    # The name/label of the Transaction
    name = models.CharField(max_length=150)

    # A more detailed message about the Transaction provided by users
    message = models.TextField()

    # Unique UUID to distinguish Transactions with the same name/payer/payee
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # The Account who pays (payer) and the Account who receives (payee)
    payer = models.OneToOneField(Account, related_name='payer', on_delete=models.CASCADE, null=True)
    payee = models.OneToOneField(Account, related_name='payee', on_delete=models.CASCADE, null=True)

    # The amount of money involved in the transaction
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # The UserGroup to which the Transaction belongs
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)

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
        return '"' + self.name + '": ' + self.payer.user.username + ' pays ' + self.payee.user.username

    def is_open(self):
        return self.status is 'O'

    def is_closed(self):
        return self.status is 'C'