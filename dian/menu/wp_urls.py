#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'menu.wp_views',

    url(r'^get-menus-by-restaurant/$', 'get_restaurant_menu_list'),

)

