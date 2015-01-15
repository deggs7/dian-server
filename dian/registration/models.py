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
    phone = models.CharField(max_length=64, null=False, blank=False)
    table_type = models.ForeignKey('restaurant.TableType', related_name="registrations")
    queue_number = models.IntegerField("queue number", default=0)
    create_time = models.DateTimeField(default=datetime.datetime.now())
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=16, choices=STATUS, default=STATUS[0][0])

    # 记录冗余信息用于后续统计
    table_min_seats = models.IntegerField("min seats", default=1)
    table_max_seats = models.IntegerField("max seats", default=1)

