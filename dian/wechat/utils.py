#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import urllib
import qrcode
import qiniu
import os
import datetime
import time

from dian.settings import APP_ID, APP_SECRET

from dian.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY
from dian.settings import QINIU_BUCKET_PUBLIC
from dian.settings import TEMP_DIR
from dian.settings import DEBUG

from wechat_sdk.basic import WechatBasic

from dian.utils import get_md5
from wechat.models import WechatStore


def create_jsapi_signature(timestamp, nonceStr, url):
    """
    创建jsapi_signature
    """
    jsapi_ticket = get_jsapi_ticket()
    wechat = WechatBasic(appid=APP_ID, appsecret=APP_SECRET,\
            jsapi_ticket=jsapi_ticket)
    signature = wechat.generate_jsapi_signature(timestamp, nonceStr, url,\
            jsapi_ticket)

    return signature


def get_jsapi_ticket():
    """
    返回jsapi_ticket，如果缓存的时间戳超过7000秒(微信过期7200)，就重新去获取
    :return: jsapi_ticket
    """
    wechat = WechatBasic(appid=APP_ID, appsecret=APP_SECRET)

    jsapi_ticket_expires_at =\
            WechatStore.objects.get_or_create(key='jsapi_ticket_expires_at')[0]
    jsapi_ticket = WechatStore.objects.get_or_create(key='jsapi_ticket')[0]
    if (not jsapi_ticket_expires_at.value or\
        not jsapi_ticket.value or\
        int(time.time()) > (int(jsapi_ticket_expires_at.value)-200)): # 多算200秒
        # 获取新jsapi_ticket
        res = wechat.grant_jsapi_ticket()
        jsapi_ticket_expires_at.value = res.get('expires_in', None)
        jsapi_ticket_expires_at.save()
        jsapi_ticket.value = res.get('ticket', None)
        jsapi_ticket.save()

        # 有点low的wechat_sdk，只要jsapi_ticket更新，就连access_token一起更新
        # 所以下面需要同时再更新一下access_token的值
        access_token_expires_at =\
                WechatStore.objects.get_or_create(key='access_token_expires_at')[0]
        access_token = WechatStore.objects.get_or_create(key='access_token')[0]
        token_res = wechat.get_access_token()
        access_token_expires_at.value = token_res.get('access_token_expires_at',\
                None)
        access_token_expires_at.save()
        access_token.value = token_res.get('access_token', None)
        access_token.save()

    return jsapi_ticket.value


def get_access_token():
    """
    返回access_token，如果超过过期时间（微信默认7200秒），就重新去获取
    """
    wechat = WechatBasic(appid=APP_ID, appsecret=APP_SECRET)

    access_token_expires_at =\
            WechatStore.objects.get_or_create(key='access_token_expires_at')[0]
    access_token = WechatStore.objects.get_or_create(key='access_token')[0]
    if (not access_token_expires_at.value or\
        not access_token.value or\
        int(time.time()) > (int(access_token_expires_at.value)-200)): # 多算200秒
        # 获取新access_token
        res = wechat.grant_token()
        access_token_expires_at.value = res['access_token_expires_at']
        access_token_expires_at.save()
        access_token.value = res['access_token']
        access_token.save()

    return access_token.value

