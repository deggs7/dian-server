#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^registration/$', views.RegistrationList.as_view()),
    url(r'^registration/(?P<pk>[0-9]+)/$', views.update_registration),

    url(r'^msg-task/$', views.create_msg_task),
]

urlpatterns += patterns(
    'registration.views',

    # for statistics report
    url(r'^statistics/daily-registration/$', 'get_daily_registration'),
    url(r'^statistics/avg-waiting-time/$', 'get_avg_waiting_time'),
    url(r'^statistics/daily-type-registration/$', 'get_daily_type_registration'),

    # for history report
    url(r'^history/today-registration/$', 'get_today_registration')
)

urlpatterns = format_suffix_patterns(urlpatterns)
