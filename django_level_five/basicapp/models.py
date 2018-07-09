# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfileInfo(models.Model):

    #create a relationship with User model instead of inheriting it
    user = models.OneToOneField(User)

    #create model attributes here
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics",blank=True)


    def __str__(self):
        return self.user.username
