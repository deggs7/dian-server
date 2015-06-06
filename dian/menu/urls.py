#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'menu.views',

    # 菜单管理相关
    url(r'^menu/$', 'create_menu'),
    url(r'^menu/$', 'list_menu'),
    url(r'^menu/(?P<pk>[0-9]+)/$', 'get_menu'),
    url(r'^menu/(?P<pk>[0-9]+)/$', 'update_menu'),
    url(r'^menu/(?P<pk>[0-9]+)/$', 'delete_menu'),

    # 分类管理相关
    url(r'^category/$', 'create_category'),
    url(r'^category/(?P<pk>[0-9]+)/$', 'get_category'),
    url(r'^category/(?P<pk>[0-9]+)/$', 'update_category'),
    url(r'^category/(?P<pk>[0-9]+)/$', 'delete_category'),
    url(r'^menu/(?P<pk>[0-9]+)/category/$', 'list_category_by_menu'),

    # 商品管理相关
    url(r'^product/$', 'create_product'),
    url(r'^product/(?P<pk>[0-9]+)/$', 'get_product'),
    url(r'^product/(?P<pk>[0-9]+)/$', 'update_product'),
    url(r'^product/(?P<pk>[0-9]+)/$', 'delete_product'),
    url(r'^category/(?P<pk>[0-9]+)/product/$', 'list_product_by_category'),

)
