#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'menu.views',

    # 菜单管理相关
    url(r'^create-menu/$', 'create_menu'),
    url(r'^list-menu/$', 'list_menu'),
    url(r'^get-menu/(?P<pk>[0-9]+)/$', 'get_menu'),
    url(r'^update-menu/(?P<pk>[0-9]+)/$', 'update_menu'),
    url(r'^delete-menu/(?P<pk>[0-9]+)/$', 'delete_menu'),

    # 分类管理相关
    url(r'^creat-category/$', 'create_category'),
    url(r'^get-category/(?P<pk>[0-9]+)/$', 'get_category'),
    url(r'^update-category/(?P<pk>[0-9]+)/$', 'update_category'),
    url(r'^delete-category/(?P<pk>[0-9]+)/$', 'delete_category'),
    url(r'^list-category-by-menu/(?P<pk>[0-9]+)/$', 'list_category_by_menu'),

    # 商品管理相关
    url(r'^create-product/$', 'create_product'),
    url(r'^get-product/(?P<pk>[0-9]+)/$', 'get_product'),
    url(r'^update-product/(?P<pk>[0-9]+)/$', 'update_product'),
    url(r'^delete-product/(?P<pk>[0-9]+)/$', 'delete_product'),
    url(r'^list-product-by-category/(?P<pk>[0-9]+)/$', 'list_product_by_category'),

)
