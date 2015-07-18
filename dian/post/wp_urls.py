# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'post.wp_views',

    url(r'^list-my-post/$', 'list_my_post'),
    url(r'^list-my-post/(?P<member_id>\w+)/$', 'list_my_post'),
    url(r'^get-overview-of-my-post/$', 'get_overview_of_my_post'),
    url(r'^get-overview-of-my-post/(?P<member_id>\w+)/$', 'get_overview_of_my_post'),
    url(r'^list-my-like/$', 'list_my_like'),
    url(r'^list-my-like/(?P<member_id>\w+)/$', 'list_my_like'),
    url(r'^get-overview-of-my-like/$', 'get_overview_of_my_like'),
    url(r'^get-overview-of-my-like/(?P<member_id>\w+)/$', 'get_overview_of_my_like'),
    # url(r'^create-post/$', 'create_post'),
    url(r'^get-next-post-list/(?P<limit>[0-9]+)/$', 'get_next_post_list'),
    url(r'^like-post/(?P<post_id>[0-9]+)/$', 'like_post'),
    url(r'^like-post/(?P<post_id>[0-9]+)/(?P<member_id>\w+)/$', 'like_post'),

    url(r'^list-tag-with-restaurant/(?P<restaurant_openid>\w+)/$', 'list_tag_with_restaurant'),
    url(r'^list-tag-with-activity/$', 'list_tag_with_activity'),
)
