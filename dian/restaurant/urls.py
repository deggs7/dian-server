#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'restaurant.views',

    url(r'^default-restaurant/$', 'get_default_restaurant'),
    url(r'^create-restaurant/$', 'create_restaurant'),
    url(r'^update-restaurant/$', 'update_restaurant'),
    url(r'^uptoken-restaurant/$', 'uptoken_default_restaurant'),

    # 获取餐厅用于取号的二维码
    url(r'^register-qrcode/$', 'get_register_qrcode'),
    url(r'^all-qrcode/$', 'get_all_qrcode'),
)

