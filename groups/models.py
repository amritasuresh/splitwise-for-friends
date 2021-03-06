# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Group
import uuid


class UserGroup(models.Model):
    """
    The UserGroup model represents groups of Accounts that can send Transactions to each other.
    """
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    # For storing group name - it does not need to be unique!
    group_name = models.CharField(max_length=80, default="")

    # Unique UUID to distinguish UserGroups with the same name
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Date of a UserGroup's creation
    created = models.DateTimeField()

    def __str__(self):
        return self.group.name
