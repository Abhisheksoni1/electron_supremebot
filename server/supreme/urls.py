"""tiago_btf_exchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from supreme import views
urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login$', views.login, name='login'),
    url(r'^setting$', views.setting, name='setting'),
    url('^task$', views.task, name='task'),
    url('^proxy$', views.proxy, name='proxy'),
    url('^profile$', views.profile, name='profile'),
    url('^edit_task$', views.newtask, name='edit_task'),
    url('^save_task$', views.save_task, name='save_task'),
    url('^save_profile$', views.save_profile, name='save_profile'),
    url('^start_task$', views.start_task, name='start_task'),
    url('^start_task/(?P<id>\d+)$', views.start_task, name='start_task'),
    url('^stop_task$', views.stop_task, name='stop_task'),
    url('^get_task$', views.get_task, name='get_task'),
    url('^get_task/(?P<id>\d+)$', views.get_task, name='get_task'),
    url('^get_profile/(?P<id>\d+)$', views.get_profile, name='get_profile'),
    url('^stop_task/(?P<id>\d+)$', views.stop_task, name='stop_task'),
    url('^delete_task$', views.delete_task, name='delete_task'),
    url('^delete_task/(?P<id>\d+)$', views.delete_task, name='delete_task'),
    url('^delete_profile$', views.delete_profile, name='delete_profile'),
    url('^delete_profile/(?P<id>\d+)$', views.delete_profile, name='delete_profile'),
    url('^add_proxy', views.add_proxy, name='add_proxy'),
    url('^start_proxy$', views.start_proxy, name='start_proxy'),
    url('^start_proxy/(?P<id>\d+)$', views.start_proxy, name='start_proxy'),
    url('^stop_proxy$', views.stop_proxy, name='stop_proxy'),
    url('^stop_proxy/(?P<id>\d+)$', views.stop_proxy, name='stop_proxy'),
    url('^delete_proxy$', views.delete_proxy, name='delete_proxy'),
    url('^delete_proxy/(?P<id>\d+)$', views.delete_proxy, name='delete_proxy'),
    url('^save_setting$', views.save_setting, name='save_setting'),
    url('^deactivate$', views.deactivate, name='deactivate'),
    url('^edit_task_new$', views.edit_task, name='edit_task_new'),
    url('^edit_profile$', views.edit_profile, name='edit_profile'),
]
