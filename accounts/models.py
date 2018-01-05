# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """
    The Account model extends the User model.
    The basic function of this model is to represent each user in the database.
    """
    # The username is unique
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # There is an image avatar associated with each Account
    avatar = models.URLField(default='img/anonymous_user.png')

    # The Account's default choice of currency
    CURRENCY_CHOICES = (
        ('EUR', 'Euro'),
        ('USD', 'US dollar'),
        ('PLN', 'Polish złoty'),
        ('INR', 'Indian rupee'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')

    def __str__(self):
        return self.user.username
