#! -*- encoding: utf-8 -*-

import datetime

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import IntegerField
from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import DateTimeField

from registration.models import Registration

from registration.models import REGISTRATION_STATUS_WAITING
from registration.models import REGISTRATION_STATUS_REPAST
from registration.models import REGISTRATION_STATUS_EXPIRED

import logging
logger = logging.getLogger('dian')


DATE_TIME_FORMAT = u'%Y-%m-%d %H:%M'

class RegistrationSerializer(ModelSerializer):
    waiting_time = SerializerMethodField(method_name="get_waiting_time")
    # phone_display = SerializerMethodField(method_name="get_phone")
    member_display = SerializerMethodField(method_name="get_member")

    class Meta:
        model = Registration
        # fields = ("id", "table_type", "queue_number", "waiting_time",\
        #         "phone_display", "status", "member_display", "reg_method")

    def get_waiting_time(self, obj):
        time_delta = datetime.datetime.now() - obj.create_time.replace(tzinfo=None)
        ret = ""

        if time_delta.days > 0:
            ret += "%d" % time_delta.days
            ret += u"天"

        if time_delta.seconds > 3600:
            hours = time_delta.seconds / 3600
            minutes = time_delta.seconds % 3600 / 60
            ret += u"%d小时%d分钟" % (hours, minutes)
        elif 60 < time_delta.seconds < 3600:
            minutes = time_delta.seconds / 60
            ret += u"%d分钟" % minutes
        else:
            ret += u"%d秒" % time_delta.seconds

        return ret

    # def get_phone(self, obj):
    #     return format_phone(obj.phone)

    def get_member(self, obj):
        try:
            rt = {
                'nickname': obj.member.wp_nickname,
                'headimgurl': obj.member.wp_headimgurl,
                'phone': _format_phone(obj.member.phone),
            }
            return rt
        except Exception, e:
            logger.error(e)
            return {}


class RegistrationHistorySerializer(ModelSerializer):
    # create_time = DateTimeField(format=DATE_TIME_FORMAT)
    # end_time = DateTimeField(format=DATE_TIME_FORMAT)
    # phone = SerializerMethodField(method_name="get_phone")
    status = SerializerMethodField(method_name="get_status_desc")
    table_name = SerializerMethodField(method_name="get_table_name")
    member_display = SerializerMethodField(method_name="get_member")

    class Meta:
        model = Registration
        # fields = ("id", "phone", "queue_number", "create_time", "end_time",\
        #         "status", "table_name", "reg_method", "member_display")

    # def get_phone(self, obj):
    #     return format_phone(obj.phone)

    def get_table_name(self, obj):
        return obj.table_type.name

    def get_status_desc(self, obj):
        desc = {
            REGISTRATION_STATUS_WAITING: u"等待中",
            # "turn": u"下一个",
            REGISTRATION_STATUS_REPAST: u"已就餐",
            REGISTRATION_STATUS_EXPIRED: u"已过号"
        }
        return desc[obj.status]

    def get_member(self, obj):
        try:
            rt = {
                'nickname': obj.member.wp_nickname,
                'headimgurl': obj.member.wp_headimgurl,
                'phone': _format_phone(obj.member.phone),
            }
            return rt
        except Exception, e:
            logger.error(e)
            return {}


class RegistrationDetailSerializer(ModelSerializer):
    """
    目前用于微信端对排号实体的展示
    """
    # create_time = DateTimeField(format=DATE_TIME_FORMAT)
    # end_time = DateTimeField(format=DATE_TIME_FORMAT)
    status = SerializerMethodField(method_name="get_status_desc")
    table_type = SerializerMethodField(method_name="get_table_type")
    restaurant = SerializerMethodField(method_name="get_restaurant")
    current_registration =\
    SerializerMethodField(method_name="get_current_registration")

    class Meta:
        model = Registration
        # fields = ("id", "queue_number", "create_time", "end_time",\
        #         "status", "table_type", "restaurant", "current_registration")

    def get_table_type(self, obj):
        try:
            rt = {
                'id': obj.table_type.id,
                'name': obj.table_type.name,
            }
            return rt
        except:
            return {}

    def get_status_desc(self, obj):
        desc = {
            REGISTRATION_STATUS_WAITING: u"等待中",
            # "turn": u"下一个",
            REGISTRATION_STATUS_REPAST: u"已就餐",
            REGISTRATION_STATUS_EXPIRED: u"已过号"
        }
        return desc[obj.status]

    def get_current_registration(self, obj):
        try:
            current_reg = obj.table_type.registrations\
                .filter(status=REGISTRATION_STATUS_WAITING).order_by('id').first()
            return current_reg.queue_number 
        except:
            return None

    def get_restaurant(self, obj):
        try:
            rt = {
                'id': obj.restaurant.id,
                'name': obj.restaurant.name,
            }
            return rt
        except:
            return {}


def _format_phone(phone):
    try:
        return phone[:3] + '*' * 4 + phone[-4:]
    except Exception, e:
        return phone

