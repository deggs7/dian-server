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
    #url(r'^remove-cart-item/$', 'remove_cart_item'),

    # 修改商品数量
    url(r'^decrease-cart-item/(?P<pk>[0-9]+)/$', 'decrease_cart_item'),

    # 创建订单
    url(r'^create-order-from-cart/(?P<cart_pk>[0-9]+)/$', 'create_order_from_cart'),

    # 取消订单(餐厅未确实前)
    url(r'^cancel-order/(?P<order_pk>[0-9]+)/$', 'cancel_order'),

    # 获取历史订单列表
    url(r'^list-order/$', 'list_order'),

    # 获取订单详细信息
    url(r'^get-detail-order/(?P<order_pk>[0-9]+)/$', 'get_detail_order')
)

