# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect

from .models import Notice, Profile
from .forms import NoticeForm, ProfileForm


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

def add_money(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.current_balance += profile.transaction
            profile.user = request.user
            profile.save()
            return redirect('/exchange')
    else:
        form = ProfileForm()
    return render(request, 'exchange/add_money.html', {'form': form})