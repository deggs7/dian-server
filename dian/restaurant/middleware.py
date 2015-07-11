#!/usr/bin/env python
# -*- coding: utf-8 -*-

from restaurant.models import Restaurant
from dian.settings import DEBUG


class RestaurantMiddleware(object):

    def process_request(self, request):
        """
        从header重读出restaurant_id, 从而获取用户当前操作的restaurant，放入request中。
        """
        restaurant_id = request.META.get('HTTP_X_RESTAURANT_ID', None)
        if restaurant_id:
            try:
                restaurant = Restaurant.objects.get(pk=restaurant_id)
                request.current_restaurant = restaurant
            except Restaurant.DoesNotExist:
                request.current_restaurant = None
        else:
            request.current_restaurant = None

        # 用于辅助接口文档的呈现
        if DEBUG and not request.current_restaurant:
            try:
                request.current_restaurant = Restaurant.objects.all()[0]
            except:
                request.current_restaurant = None

        return
