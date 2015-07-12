#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dian.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # 框架提供接口
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',\
        namespace='rest_framework')),
    url(r'^api-token-auth/',\
        'rest_framework.authtoken.views.obtain_auth_token'),


    # 各业务模块
    url(r'^account/', include('account.urls')),
    url(r'^restaurant/', include('restaurant.urls')),
    url(r'^registration/', include('registration.urls')),
    url(r'^table/', include('table.urls')),
    url(r'^menu/', include('menu.urls')),
    url(r'^trade/', include('trade.urls')),
    url(r'^reward/', include('reward.urls')),
    url(r'^post/', include('post.urls')),

    url(r'^captcha/$', views.captcha),
    url(r'^reset-passwd/$', views.reset_passwd),


    # 微信接口统一在此
    url(r'^wp/', include('dian.wp_urls')),


    # Swagger Documentation Generator for Django REST Framework
    # https://github.com/marcgibbons/django-rest-swagger
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
