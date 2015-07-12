#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dian.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    
    # 业务模块
    url(r'^account/', include('account.wp_urls')),
    url(r'^menu/', include('menu.wp_urls')),
    url(r'^registration/', include('registration.wp_urls')),
    url(r'^restaurant/', include('restaurant.wp_urls')),
    url(r'^table/', include('table.wp_urls')),
    url(r'^trade/', include('trade.wp_urls')),
    url(r'^wechat/', include('wechat.wp_urls')),
    url(r'^reward/', include('reward.wp_urls')),
)
