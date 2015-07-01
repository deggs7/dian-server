#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


# console端接口
urlpatterns = patterns(
    'trade.views',

    # # 获取订单列表
    # url(r'^list-order/$', 'list_order'),

    # 确认订单
    url(r'^confirm-order/(?P<order_pk>[0-9]+)/$', 'confirm_order'),

    # 退回订单
    url(r'^reject-order/(?P<order_pk>[0-9]+)/$', 'reject_order'),

    # 结束订单(已结账)
    url(r'^finish-order/(?P<order_pk>[0-9]+)/$', 'finish_order'),
)
