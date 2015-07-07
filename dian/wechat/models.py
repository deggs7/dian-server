#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class WechatStore(models.Model):
    """
    对微信接口调用中用到的token等进行缓存
    """

    key = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)

    # access_token = models.CharField(max_length=255, blank=True, null=True)
    # access_token_expires_at = models.CharField(max_length=255, blank=True, null=True)
    # jsapi_ticket = models.CharField(max_length=255, blank=True, null=True)
    # jsapi_ticket_expires_at = models.CharField(max_length=255, blank=True, null=True)
    
