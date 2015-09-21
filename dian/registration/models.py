#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime
from django.db import models

REG_METHOD_PHONE = 0
REG_METHOD_WECHAT = 1

REGISTRATION_STATUS_WAITING = 0
REGISTRATION_STATUS_REPAST = 1
REGISTRATION_STATUS_EXPIRED = 2

REGISTRATION_STATUS = (
    (REGISTRATION_STATUS_WAITING, 'Waiting'),
    (REGISTRATION_STATUS_REPAST , 'Repast'),
    (REGISTRATION_STATUS_EXPIRED , 'Expired'),
)

class Registration(models.Model):

    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=REGISTRATION_STATUS,\
            default=REGISTRATION_STATUS_WAITING)
    restaurant = models.ForeignKey('restaurant.Restaurant',\
            related_name="registrations")
    # 顾客成员(通过短信或微信取号的)
    # member = models.ForeignKey('account.Member', related_name="members", null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey('account.Member', related_name="members")

    # 记录table_type信息，固化号单状态，用于后续统计
    queue_name = models.CharField(max_length=255, blank=True, null=True)
    queue_number = models.IntegerField("queue number", blank=True, null=True)
    table_min_seats = models.IntegerField("min seats", blank=True, null=True)
    table_max_seats = models.IntegerField("max seats", blank=True, null=True)

    # 取号方式 0: 手机取号  1: 微信取号
    reg_method = models.IntegerField("register method", default=REG_METHOD_PHONE)

    # 此 table_type 只是临时存储，不可以被直接引用（最好去除此属性）
    # TODO 微信端已清理对此属性依赖，console端还未处理
    table_type = models.ForeignKey('table.TableType',
            related_name="registrations", blank=True, null=True)
    
    # TODO 需去除此属性，统一走member获取
    phone = models.CharField(max_length=255, null=True, blank=True)


    def get_current_number(self):
        try:
            current_reg = self.table_type.registrations\
                .filter(status=REGISTRATION_STATUS_WAITING).order_by('id').first()
            return current_reg.queue_number
        except:
            return 0

