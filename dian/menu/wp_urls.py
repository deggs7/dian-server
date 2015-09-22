#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'menu.wp_views',

    url(r'^list-menu-by-table/$', 'list_menu_by_table'),

)

