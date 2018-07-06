# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from django.db import transaction

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer, NoticeSerializer, ProfileSerializer


from .models import Notice, Profile
from .forms import NoticeForm, ProfileForm, SetExecutorForm, DoneForm

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().all()
    serializer_class = UserSerializer

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('pub_date')
    serializer_class = UserSerializer

class IndexView(generic.ListView):
    template_name = 'exchange/index.html'
    context_object_name = 'latest_notice_list'

    @transaction.atomic
    def get_queryset(self):
        return Notice.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Notice
    template_name = 'exchange/detail.html'


class NewView(generic.CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'exchange/new.html'

    @transaction.atomic
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewView, self).form_valid(form)
    
    @transaction.atomic
    def get_success_url(self):
        return reverse("exchange:detail", kwargs={'pk': self.object.pk})

class EditView(generic.UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'exchange/new.html'

    @transaction.atomic
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(EditView, self).form_valid(form)
    
    @transaction.atomic
    def get_success_url(self):
        return reverse("exchange:detail", kwargs={'pk': self.object.pk})

class UserNoticesView(generic.ListView):
    template_name = 'exchange/user_notices.html'
    context_object_name = 'notices'

    @transaction.atomic
    def get_queryset(self):
        return Notice.objects.filter(author=self.request.user)

class AddMoneyView(generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "exchange/add_money.html"
    
    @transaction.atomic
    def get_success_url(self):
        return reverse("exchange:index")

    @transaction.atomic
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.current_balance += form.instance.transaction_sum
        return super(AddMoneyView, self).form_valid(form)


class UserTasksView(generic.ListView):
    template_name = 'exchange/user_tasks.html'
    context_object_name = 'notices'

    @transaction.atomic
    def get_queryset(self):
        return Notice.objects.filter(executor=self.request.user)

class SetExecutorView(generic.UpdateView):
    model = Notice
    form_class = SetExecutorForm
    
    @transaction.atomic
    def form_valid(self, form):
        form.instance.executor = self.request.user
        return super(SetExecutorView, self).form_valid(form)
    
    @transaction.atomic
    def get_success_url(self):
        return reverse("exchange:detail", kwargs={'pk': self.object.pk})

@transaction.atomic
def done(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    author = Profile.objects.get(user=notice.author)
    executor = Profile.objects.get(user=notice.executor)
    if request.method == "POST":
        form = DoneForm(request.POST)
        if form.is_valid():
            notice.done = True
            if author.current_balance >= notice.price:
                author.current_balance -= notice.price
                executor.current_balance += notice.price
                notice.save()
                author.save()
                executor.save()
                return redirect('exchange:detail', pk=notice.pk)
            else:
                return redirect('exchange:add_money', pk=author.pk)