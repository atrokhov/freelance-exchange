# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from djmoney.models.fields import MoneyField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Transactions_types(models.Model):
    type = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Типы транзакций'

    def __unicode__(self):
        return self.type

class Transactions(models.Model):
    transaction_type = models.ForeignKey(Transactions_types)
    transaction_sum = models.IntegerField()

    class Meta:
        verbose_name = 'Транзакции'



class Notice(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=200, default="")
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    price = models.IntegerField()
    executor = models.ForeignKey(User, null=True, blank=True, related_name='author')

    def __str__(self):
        return self.title
        return self.body

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(default=0)
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE)


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()
