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

