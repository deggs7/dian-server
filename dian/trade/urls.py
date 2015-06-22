#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


# 微信端接口
urlpatterns = patterns(
    'trade.wp_views',

    # 获取指定餐厅的购物车
    url(r'^get-cart-by-restaurant/$', 'get_cart_by_restaurant'),

    # 添加一个商品至购物车
    url(r'^add-cart-item/$', 'add_cart_item'),

    # 从购物车移除一个商品
    url(r'^remove-cart-item/$', 'remove_cart_item'),

    # 修改商品数量
    url(r'^recount-cart-item/$', 'recount_cart_item'),

    # 创建订单
    url(r'^create-order-from-cart/(?P<cart_pk>[0-9]+)/$', 'create_order_from_cart'),

    # 取消订单(餐厅未确实前)
    url(r'^cancel-order/(?P<order_pk>[0-9]+)/$', 'cancel_order'),

    # 获取历史订单列表
    url(r'^get-order-list/$', 'get_order_list'),

    # 获取订单详细信息
    url(r'^get-order-detail/(?P<order_pk>[0-9]+)/$', 'get_order_detail')
)

# console端接口
urlpatterns += patterns(
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
