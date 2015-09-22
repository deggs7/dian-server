#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


# 微信端接口
urlpatterns = patterns(
    'trade.wp_views',

    # 获取当前订单列表
    url(r'^list-current-order/$', 'list_current_order'),

    # 获取订单详细信息
    url(r'^get-detail-order/$', 'get_detail_order'),

    # 获取历史订单列表
    url(r'^list-history-order/$', 'list_history_order'),

    # 根据id获取购物车
    url(r'^get-cart/$', 'get_cart'),

    # 根据餐桌id获取该餐厅的购物车
    url(r'^get-cart-by-table/$', 'get_cart_by_table'),

    # 更新购物车
    url(r'^update-cart/(?P<cart_pk>[0-9]+)/$', 'update_cart'),

    # 创建订单
    url(r'^create-order-from-cart/$', 'create_order_from_cart'),

    # 取消订单(餐厅未确实前)
    url(r'^cancel-order/(?P<order_pk>[0-9]+)/$', 'cancel_order'),

    # 添加一个商品至购物车
    # url(r'^add-cart-item/$', 'add_cart_item'),

    # 从购物车移除一个商品
    #url(r'^remove-cart-item/$', 'remove_cart_item'),

    # 修改商品数量
    # url(r'^decrease-cart-item/(?P<pk>[0-9]+)/$', 'decrease_cart_item'),



)

