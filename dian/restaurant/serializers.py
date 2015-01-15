#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import TableType
from .models import Restaurant
from registration.serializers import RegistrationSerializer


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "file_key", "create_time", "owner")


class TableTypeSerializer(ModelSerializer):

    class Meta:
        model = TableType
        fields = ("id", "name", "min_seats", "max_seats")


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
        queue_registrations = obj.registrations.filter(status='waiting').order_by('queue_number')
        return [RegistrationSerializer(reg).data for reg in queue_registrations]

    def get_slug(self, obj):
        return obj.name + u"（" + "%d" % obj.min_seats + u"-" + "%d" % obj.max_seats + u"人）"




