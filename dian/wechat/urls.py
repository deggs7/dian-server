#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


# 对接微信server
urlpatterns = patterns(
    'wechat.views',

    url(r'^receive-message/$', 'receive_message'),

)
