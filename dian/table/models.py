#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Table(models.Model):
    """
    餐桌
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    restaurant = models.ForeignKey('restaurant.Restaurant', related_name="tables", null=True, blank=True)
    table_type = models.ForeignKey('table.TableType', related_name="tables", null=True)

    # 餐桌在就餐过程中的信息和状态
    order = models.OneToOneField('trade.Order', null=True, blank=True, related_name="table")
    # status = models.IntegerField(choices=STATUS, default=STATUS[0][0])


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
        return self.registrations.filter(status='waiting').count()

