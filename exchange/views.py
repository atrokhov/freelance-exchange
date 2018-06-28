# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Notice
from .forms import NoticeForm, SignUpForm, ProfileForm

from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def index(request):
    latest_notice_list = Notice.objects.order_by('-pub_date')
    context = {'latest_notice_list': latest_notice_list}
    return render(request, 'exchange/index.html', context)

def your_notices(request):
    logged_in_user = request.user
    logged_in_user_notices = Notice.objects.filter(author=logged_in_user)

    return render(request, 'exchange/user_notices.html', {'notices': logged_in_user_notices})

def detail(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    return render(request, 'exchange/detail.html', {'notice': notice})

def new(request):
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return redirect('/exchange')
    else:
        form = NoticeForm()
    return render(request, 'exchange/new.html', {'form': form})

def edit(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.method == "POST":
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return render(request, 'exchange/detail.html', {'notice': notice})
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'exchange/new.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/exchange')
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})