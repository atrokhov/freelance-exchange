# -*- coding: utf-8 -*-
from django import forms

from .models import Notice, Profile


class NoticeForm(forms.ModelForm):

    class Meta:
        model = Notice
        fields = ('title', 'body', 'price',)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('transaction_sum',)