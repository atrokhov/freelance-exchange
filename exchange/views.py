# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.db import transaction

from .models import Notice, Profile
from .forms import NoticeForm, ProfileForm


class IndexView(generic.ListView):
    template_name = 'exchange/index.html'
    context_object_name = 'latest_notice_list'

    def get_queryset(self):
        return Notice.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Notice
    template_name = 'exchange/detail.html'


class NewView(generic.CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'exchange/new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse("exchange:detail", kwargs={'pk': self.object.pk})

class EditView(generic.UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'exchange/new.html'
    
    def get_success_url(self):
        return reverse("exchange:detail", kwargs={'pk': self.pk})

class UserNoticesView(generic.ListView):
    template_name = 'exchange/user_notices.html'
    context_object_name = 'notices'

    def get_queryset(self):
        return Notice.objects.filter(author=self.request.user)

class AddMoneyView(generic.FormView):
    model = Profile
    form_class = ProfileForm
    template_name = "exchange/add_money.html"
    
    def get_success_url(self):
        return reverse("exchange:index")

    


            

