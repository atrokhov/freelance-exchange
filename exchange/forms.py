# -*- coding: utf-8 -*-
from django import forms

from .models import Notice, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NoticeForm(forms.ModelForm):

    class Meta:
        model = Notice
        fields = ('title', 'body', 'price',)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Необязательно.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Необязательно.')
    email = forms.EmailField(max_length=254, help_text='Обязательно.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    money = forms.IntegerField(required=False)

    class Meta:
        model = Profile
        fields = ('money', )