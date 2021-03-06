#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random

from django.db import models
from registration.models import REGISTRATION_STATUS_WAITING

from dian.settings import MD5_SEED
from dian.utils import get_md5

class Table(models.Model):
    """
    餐桌
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    restaurant = models.ForeignKey('restaurant.Restaurant', related_name="tables", null=True, blank=True)
    table_type = models.ForeignKey('table.TableType', related_name="tables", null=True)
    openid = models.CharField(max_length=255, blank=True, null=True)

    # 餐桌在就餐过程中的信息和状态
    order = models.OneToOneField('trade.Order', null=True, blank=True, related_name="table")
    # status = models.IntegerField(choices=STATUS, default=STATUS[0][0])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.openid = get_md5("%s-%s-%s" % (MD5_SEED,\
                datetime.datetime.now(), random.random()))
        super(Table, self).save(*args, **kwargs)


class TableType(models.Model):
    """
    餐桌类型
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    min_seats = models.IntegerField("min seats", default=1)
    max_seats = models.IntegerField("max seats", default=1)
    restaurant = models.ForeignKey('restaurant.Restaurant', related_name="table_types", null=True)
    next_queue_number = models.IntegerField(default=1, blank=False, null=False)

    def get_registration_left(self):
        """
        TODO: 此方法缺陷较大，需进一步完善
        """
        return self.registrations.filter(status=REGISTRATION_STATUS_WAITING).count()

    def next_queue(self):
        """
        餐桌排队号码+1
        """
        self.next_queue_number += 1
        self.save()

