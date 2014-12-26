#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from account import views


urlpatterns = patterns(
    'account.views',

    url(r'^my-account/$', 'get_my_account'),

)

