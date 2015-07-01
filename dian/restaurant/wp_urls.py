#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'restaurant.wp_views',

    url(r'^get-restaurant/$', 'get_restaurant'),

)
