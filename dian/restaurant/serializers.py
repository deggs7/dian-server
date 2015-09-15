#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from restaurant.models import Restaurant


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        # fields = ("id", "name", "file_key", "create_time", "owner", "wp_name",\
        #         "wp_qrcode_file_key", "wifi_name", "wifi_password")

