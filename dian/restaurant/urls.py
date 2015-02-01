#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'restaurant.views',

    url(r'^default-restaurant/$', 'get_default_restaurant'),
    url(r'^create-restaurant/$', 'create_restaurant'),
    url(r'^update-restaurant/$', 'update_restaurant'),
    url(r'^uptoken-restaurant/$', 'uptoken_default_restaurant'),

    url(r'^table-type/$', 'list_or_create_table_type'),
    url(r'^table-type/(?P<pk>[0-9]+)/$', 'get_or_update_table_type'),
    url(r'^table-type-details/$', 'list_table_type_details'),

    # for statistics report
    url(r'^statistics/daily-registration/$', 'get_daily_registration'),
    url(r'^statistics/avg-waiting-time/$', 'get_avg_waiting_time'),
    url(r'^statistics/daily-type-registration/$', 'get_daily_type_registration')
)
