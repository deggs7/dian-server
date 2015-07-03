#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime
from django.db import models


class Registration(models.Model):
    STATUS = (
        ('waiting', 'Waiting'),
        ('turn', 'Turn'),
        ('expired', 'Expired'),
        ('passed', 'Passed'),
    )

    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    queue_name = models.CharField(max_length=255, blank=True, null=True)
    queue_number = models.IntegerField("queue number", default=0)
    create_time = models.DateTimeField(default=datetime.datetime.now())
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=16, choices=STATUS, default=STATUS[0][0])

    # 此 table_type 只是临时存储，不可以被直接引用（最好去除此属性）
    table_type = models.ForeignKey('table.TableType', related_name="registrations")
    
    # 记录冗余信息用于后续统计
    table_min_seats = models.IntegerField("min seats", default=1)
    table_max_seats = models.IntegerField("max seats", default=1)

    restaurant = models.ForeignKey('restaurant.Restaurant', related_name="registrations", null=True)

    # 顾客成员(通过短信或微信取号的)
    member = models.ForeignKey('account.Member', related_name="members",\
            null=True, on_delete=models.SET_NULL)

    # 取号方式 0: 手机取号  1: 微信取号
    reg_method = models.IntegerField("register method", default=0)

    def get_current_number(self):
        try:
            current_reg = self.table_type.registrations.filter(status='turn').first()
            return current_reg.queue_number
        except:
            return 0


class Strategy(models.Model):
    """
    超时策略，目前支持礼物和折扣两种模式
    """
    REWARD_TYPE = (
        ('gift', 'Gift'),
        ('discount', 'Discount'),
    )

    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey("restaurant.Restaurant", related_name="strategies", null=True)

    time_wait = models.IntegerField("waiting time in minutes", null=False, blank=False)
    reward_type = models.CharField(max_length=16, choices=REWARD_TYPE, default=REWARD_TYPE[0][0])
    reward_info = models.CharField(max_length=512, blank=False, null=False)


class StrategyDup(models.Model):
    """
    超时策略副本，目前支持礼物和折扣两种模式
    用于关联registration，registration被应用Strategy后，使用该表复制信息和关联
    规避用户删除Strategy后的信息丢失
    """
    REWARD_TYPE = (
        ('gift', 'Gift'),
        ('discount', 'Discount'),
    )

    id = models.AutoField(primary_key=True)
    strategy_id = models.BigIntegerField(null=False, blank=False)
    time_wait = models.IntegerField("waiting time in minutes", null=False, blank=False)
    reward_type = models.CharField(max_length=16, choices=REWARD_TYPE, default=REWARD_TYPE[0][0])
    reward_info = models.CharField(max_length=512, blank=False, null=False)
    registration = models.ForeignKey(Registration, null=False, related_name="strategies")


