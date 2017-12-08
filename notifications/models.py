# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Account
from groups.models import UserGroup
from transactions.models import Transaction
from datetime import datetime
import uuid


class Notification(models.Model):
    # Unique UUID to distinguish Notifications
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Contents of the notification
    message = models.TextField()

    # Many Accounts can have many Notifications
    accounts = models.ManyToManyField(Account)

    group = models.OneToOneField(UserGroup, on_delete=models.CASCADE)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)

    # Date/time of notification's creation
    created = models.DateTimeField(default=datetime.now, blank=True)

    # The type of the notification
    TYPE_CHOICES = (
        ('TC', 'TRANSACTION CREATED'),
        ('TE', 'TRANSACTION EDITED'),
        ('TF', 'TRANSACTION FINISHED'),
        ('GA', 'ADDED TO GROUP'),
        ('GR', 'REMOVED FROM GROUP'),
        ('GD', 'GROUP DELETED')
    )
    status = models.CharField(max_length=2, choices=TYPE_CHOICES)

    def __str__(self):
        return self.message
