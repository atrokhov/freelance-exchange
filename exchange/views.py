# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Notice
from .forms import NoticeForm

from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def index(request):
    latest_notice_list = Notice.objects.order_by('-pub_date')
    context = {'latest_notice_list': latest_notice_list}
    return render(request, 'exchange/index.html', context)

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

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})