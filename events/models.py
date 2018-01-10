# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from groups.models import UserGroup
import uuid
from datetime import datetime


# Create your models here.
class Event(models.Model):
    """
    The Event model represents an event that may contain one or more Transactions within a Group.
    """

    # The name of the Event
    name = models.CharField(max_length=150)

    # Unique UUID to distinguish Events with the same name
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # The UserGroup to which the Event belongs
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)

    # The date/time that this transaction was created/finished
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        """
        This function returns the event name in order to represent the Event as a string.
        :return: A string representing the Event
        """
        return self.name