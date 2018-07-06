# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from djmoney.models.fields import MoneyField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Notice(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=200, default="")
    body = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    price = models.IntegerField(null=True, blank=True)
    executor = models.ForeignKey(User, null=True, blank=True, related_name='author')

    class Meta:
        verbose_name = 'Объявления'

    def __str__(self):
        return self.title
        return self.body

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(default=0, null=True, blank=True)
    transaction_sum = models.IntegerField(null=True, blank=True)

    @receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
    def save_profile(sender, instance, created, **kwargs):
        user = instance
        if created:
            profile = Profile(user=user)
            profile.save()