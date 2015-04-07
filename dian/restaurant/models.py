#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random

from django.db import models
from account.models import User

from dian.settings import MD5_SEED
from dian.utils import get_md5


class Restaurant(models.Model):
    """
    餐厅实体

    name: 餐厅名称
    file_key: 上传七牛的文件key
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    file_key = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name="own_restaurants")
    openid = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.openid = get_md5("%s-%s-%s" % (MD5_SEED,\
                datetime.datetime.now(), random.random()))
        super(Restaurant, self).save(*args, **kwargs)


class TableType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    min_seats = models.IntegerField("min seats", default=1)
    max_seats = models.IntegerField("max seats", default=1)
    restaurant = models.ForeignKey(Restaurant, related_name="table_types", null=True)
    next_queue_number = models.IntegerField(default=1, blank=False, null=False)

    def get_registration_left(self):
        """
        TODO: 此方法缺陷较大，需进一步完善
        """
        return self.registrations.filter(status='waiting').count()


class Strategy(models.Model):
    """
    超时策略，目前支持礼物和折扣两种模式
    """
    REWARD_TYPE = (
        ('gift', 'Gift'),
        ('discount', 'Discount'),
    )

    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, related_name="strategies", null=True)

    time_wait = models.IntegerField("waiting time in minutes", null=False, blank=False)
    reward_type = models.CharField(max_length=16, choices=REWARD_TYPE, default=REWARD_TYPE[0][0])
    reward_info = models.CharField(max_length=512, blank=False, null=False)
