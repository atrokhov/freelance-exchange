from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.EditView.as_view(), name='edit'),
    url(r'^add_money/$', views.AddMoneyView.as_view(), name='add_money'),
    url(r'^notice/new/$', views.NewView.as_view(), name='new'),
    url(r'^your_notices/$', views.UserNoticesView.as_view(), name='your_notices'),
]