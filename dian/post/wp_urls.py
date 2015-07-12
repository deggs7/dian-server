# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'post.views',

    url(r'^list-post/$', 'list_post'),
    url(r'^create-post/$', 'create_post'),
    url(r'^get-post/(?P<pk>[0-9]+)/$', 'get_post'),
    url(r'^update-post/(?P<pk>[0-9]+)/$', 'update_post'),
    url(r'^delete-post/(?P<pk>[0-9]+)/$', 'delete_post'),
)
