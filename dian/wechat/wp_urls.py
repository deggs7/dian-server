#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'wechat.wp_views',

    url(r'^get-jsapi-signature/$', 'get_jsapi_signature'),

)
