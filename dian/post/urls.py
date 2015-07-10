# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'post.views',

    url(r'^list-image/$', 'list_image'),
    url(r'^create-image/$', 'create_image'),
    url(r'^get-image/(?P<pk>[0-9]+)/$', 'get_image'),
    url(r'^update-image/(?P<pk>[0-9]+)/$', 'update_image'),
    url(r'^delete-image/(?P<pk>[0-9]+)/$', 'delete_image'),

    url(r'^list-tag/$', 'list_tag'),
    url(r'^create-tag/$', 'create_tag'),
    url(r'^get-tag/(?P<pk>[0-9]+)/$', 'get_tag'),
    url(r'^update-tag/(?P<pk>[0-9]+)/$', 'update_tag'),
    url(r'^delete-tag/(?P<pk>[0-9]+)/$', 'delete_tag'),

    url(r'^list-post/$', 'list_post'),
    url(r'^create-post/$', 'create_post'),
    url(r'^get-post/(?P<pk>[0-9]+)/$', 'get_post'),
    url(r'^update-post/(?P<pk>[0-9]+)/$', 'update_post'),
    url(r'^delete-post/(?P<pk>[0-9]+)/$', 'delete_post'),
)
