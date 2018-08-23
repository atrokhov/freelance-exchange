from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.EditView.as_view(), name='edit'),
    url(r'^add_money/(?P<pk>[0-9]+)/$', views.AddMoneyView.as_view(), name='add_money'),
    url(r'^notice/new/$', views.NewView.as_view(), name='new'),
    url(r'^your_notices/$', views.UserNoticesView.as_view(), name='your_notices'),
    url(r'^your_tasks/$', views.UserTasksView.as_view(), name='your_tasks'),
    url(r'^set_executor/(?P<pk>[0-9]+)/$', views.SetExecutorView.as_view(), name='set_executor'),
    url(r'^done/(?P<pk>[0-9]+)/$', views.done, name='done'),
]
