#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns

#weixin api
urlpatterns = patterns(
    'registration.wp_views',

    url(r'^confirm-table-type/$', 'confirm_table_type'),

    url(r'^list-current-registration/$', 'list_current_registration'),
    url(r'^list-current-registration-by-restaurant/$',\
        'list_current_registration_by_restaurant'),
    url(r'^list-history-registration/$', 'list_history_registration'),
    url(r'^get-detail-registration/$', 'get_detail_registration'),
    
)

