#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from django.db import models


class Regstration(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=64, null=False, blank=False)
    table_type = models.ForeignKey("restaurant.TableType", null=False, blank=False, related_name='registrations')
    queue_number = models.IntegerField("queue number", default=0)
    table = models.OneToOneField("restaurant.Table", null=True, blank=True, related_name='registration')

    expire = models.BooleanField(default=False)

