# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'photo.wp_views',

    url(r'^get-next-photo-list/$', 'get_next_photo_list'),
    url(r'^like-photo/(?P<photo_id>[0-9]+)/$', 'like_photo'),

    url(r'^list-tag-with-restaurant/(?P<restaurant_openid>\w+)/$', 'list_tag_with_restaurant'),
    url(r'^list-tag-with-activity/$', 'list_tag_with_activity'),
    url(r'^create-photo/$', 'create_photo'),

    url(r'^get-overview-of-my-photo/$', 'get_overview_of_my_photo'),
    url(r'^list-my-photo/$', 'list_my_photo'),

    url(r'^get-overview-of-my-like/$', 'get_overview_of_my_like'),
    url(r'^list-my-like/$', 'list_my_like'),

)
