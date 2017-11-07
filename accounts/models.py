from django.db import models
from django.contrib.auth.models import User

#The account model extends the User model. The basic function of this model is to represent each user

class Account(models.Model):

    #username is unique
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #there is an image associated to each account
    avatar = models.URLField(default='img/anonymous_user.png')

    def __str__(self):
        return self.user.username
