#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'table.wp_views',

    url(r'^list-table-type-by-restaurant/$', 'list_table_type_by_restaurant'),

)
