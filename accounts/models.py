from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """
    The Account model extends the User model.
    The basic function of this model is to represent each user in the database.
    """
    # The username is unique
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # There is an image avatar associated with each account
    avatar = models.URLField(default='img/anonymous_user.png')

    def __str__(self):
        return self.user.username
