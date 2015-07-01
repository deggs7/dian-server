#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns

#weixin api
urlpatterns = patterns(
    'registration.wp_views',

    url(r'^confirm-table-type/$', 'confirm_table_type'),
)

