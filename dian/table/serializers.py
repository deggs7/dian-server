#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from table.models import TableType
from table.models import Table
from registration.serializers import RegistrationSerializer


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


class TableSerializer(ModelSerializer):

    class Meta:
        fields = ("id", "name", "table_type")
        model = Table


class TableDetailSerializer(ModelSerializer):
    table_type_desc = SerializerMethodField(method_name="get_table_type_slug")

    class Meta:
        model = Table
        fields = ("id", "name", "restaurant", "table_type", "table_type_desc")

    def get_table_type_slug(self, obj):
        table_type = obj.table_type
        return table_type.name + u"（" + "%d" % table_type.min_seats + u"-" + "%d" % table_type.max_seats + u"人）"
