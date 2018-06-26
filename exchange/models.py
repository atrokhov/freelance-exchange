# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Notice(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    price = models.IntegerField()

    def __str__(self):
        return self.title
        return self.body