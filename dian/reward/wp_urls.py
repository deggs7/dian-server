#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'reward.wp_views',

    url(r'^get-reward-strategy-by-restaurant/$', 'get_reward_strategy_by_restaurant'),
    url(r'^determine-reward/$', 'determine_reward'),
    url(r'^list-coupons/$', 'list_coupons'),
)
