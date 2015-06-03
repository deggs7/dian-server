#!/usr/bin/env python
# -*- coding: utf-8 -*-

from restaurant.models import Restaurant


class RestaurantMiddleware(object):

    def process_request(self, request):
        """
        从header重读出restaurant_id, 从而获取用户当前操作的restaurant，放入request中。
        """
        if request.META.get('HTTP_AUTHORIZATION'):
            restaurant_id = request.META.get('HTTP_X_RESTAURANT_ID', None)
            if restaurant_id:
                try:
                    restaurant = Restaurant.objects.get(pk=restaurant_id)
                    request.current_restaurant = restaurant
                except Restaurant.DoesNotExist:
                    request.current_restaurant = None
            else:
                request.current_restaurant = None
        return
