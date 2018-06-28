from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<notice_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<notice_id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^notice/new/$', views.new, name='new'),
    url(r'^your_notices/$', views.your_notices, name='your_notices'),
]