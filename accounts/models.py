from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField(default='img/anonymous_user.png')

    def __str__(self):
        return self.user.username
