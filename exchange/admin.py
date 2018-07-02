# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Transactions, Transactions_types, Profile, Notice

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'transaction_sum')

admin.site.register(Transactions, TransactionsAdmin)
admin.site.register(Transactions_types)
admin.site.register(Profile)
admin.site.register(Notice)
