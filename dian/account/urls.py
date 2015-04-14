#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from account import views


urlpatterns = patterns(
    'account.views',

    url(r'^my-account/$', 'get_my_account'),
    url(r'^password/$', 'change_passwd'),

    url(r'^create-seed-user/$', 'create_seed_user'),
)

