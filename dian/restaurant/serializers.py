#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import TableType
from .models import Restaurant
from .models import Strategy
from registration.serializers import RegistrationSerializer


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "file_key", "create_time", "owner")


class TableTypeSerializer(ModelSerializer):
    front_left = SerializerMethodField(method_name="get_front_left")

    class Meta:
        model = TableType
        fields = ("id", "name", "min_seats", "max_seats", "front_left", "next_queue_number")

    def get_front_left(self, obj):
        return obj.get_registration_left() - 1


class TableTypeDetailSerializer(ModelSerializer):
    queue_registrations = SerializerMethodField(method_name='get_queue_registrations')
    current_registration = SerializerMethodField(method_name='get_current_registration')
    slug = SerializerMethodField(method_name="get_slug")

    class Meta:
        model = TableType
        fields = ("id", "name", "slug", "queue_registrations", "current_registration")

    def get_current_registration(self, obj):
        try:
            current_reg = obj.registrations.filter(status='turn').first()
            return RegistrationSerializer(current_reg).data if current_reg else None
        except:
            return None

    def get_queue_registrations(self, obj):
        queue_registrations = obj.registrations.filter(status='waiting').order_by('id')
        return [RegistrationSerializer(reg).data for reg in queue_registrations]

    def get_slug(self, obj):
        return obj.name + u"（" + "%d" % obj.min_seats + u"-" + "%d" % obj.max_seats + u"人）"


class StrategySerializer(ModelSerializer):
    reward_type_desc = SerializerMethodField(method_name='get_reward_type_desc')

    class Meta:
        model = Strategy
        fields = ("id", "time_wait", "reward_type", "reward_info", "reward_type_desc")

    def get_reward_type_desc(self, obj):
        desc = {
            "gift": "赠送礼物",
            "discount": "消费折扣"
        }
        return desc[obj.reward_type]
