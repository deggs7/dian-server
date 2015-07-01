#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns

#weixin api
urlpatterns = patterns(
    'account.wp_views',

    url(r'^get-member/$', 'get_member'),
)

