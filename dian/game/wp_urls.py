#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'game.wp_views',

    # url(r'^get-game-with-restaurant/$', 'get_detail_game'),
    url(r'^list-game-by-restaurant/$', 'list_game_by_restaurant'),

)
