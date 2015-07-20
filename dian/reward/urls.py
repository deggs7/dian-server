#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


# console端接口
urlpatterns = patterns(
    'reward.views',

    # 策略
    url(r'^list-strategy/$', 'list_strategy'),
    url(r'^create-strategy/$', 'create_strategy'),
    url(r'^update-strategy/(?P<pk>[0-9]+)/$', 'update_strategy'),
    url(r'^delete-strategy/(?P<pk>[0-9]+)/$', 'delete_strategy'),

    # 奖品
    url(r'^list-reward/$', 'list_reward'),
    url(r'^create-reward/$', 'create_reward'),
    url(r'^update-reward/(?P<pk>[0-9]+)/$', 'update_reward'),
    url(r'^delete-reward/(?P<pk>[0-9]+)/$', 'delete_reward'),

    # 兑换
    url(r'^get-coupon-by-code/$', 'get_coupon_by_code'),
    url(r'^exchange-coupon/(?P<pk>[0-9]+)/$', 'exchange_coupon'),
)
