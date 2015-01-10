#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from account.models import User


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


class TableType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    min_seats = models.IntegerField("min seats", default=1)
    max_seats = models.IntegerField("max seats", default=1)
    restaurant = models.ForeignKey(Restaurant, related_name="table_types", null=True)


class Table(models.Model):
    TABLE_STATUS = (
        ('dining', 'Dining'),
        ('waiting', 'Waiting'),
        ('booked', 'Booked'),
        ('idle', 'Idle')
    )
    id = models.AutoField(primary_key=True)
    table_number = models.CharField(max_length=255, blank=False, null=False)
    table_type = models.ForeignKey(TableType, null=False, related_name='tables')
    status = models.CharField(max_length=12, choices=TABLE_STATUS, default=TABLE_STATUS[-1][0])
    restaurant = models.ForeignKey(Restaurant, related_name="tables", null=True)

