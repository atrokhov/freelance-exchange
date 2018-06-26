# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Notice
from .forms import NoticeForm

class IndexView(generic.ListView):
    template_name = 'exchange/index.html'
    context_object_name = 'latest_notice_list'

    def get_queryset(self):
        return Notice.objects.order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Notice
    template_name = 'exchange/detail.html'

class CreateView(generic.CreateView):
    form_class = NoticeForm
    model = Notice
    template_name = 'exchange/new.html'

    def new(request):
        if request.method == "POST":
            form = NoticeForm(request.POST)
            if form.is_valid():
                notice = form.save(commit=False)
                post.save()
                return redirect('index')
        else:
            form = PostForm()
        return render(request, 'exchange/new.html', {'form': form})