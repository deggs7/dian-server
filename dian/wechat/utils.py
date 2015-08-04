#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import urllib
import qrcode
import qiniu
import os
import datetime
import time

from dian.settings import APP_ID, APP_SECRET, WP_DOMAIN

from dian.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY
from dian.settings import QINIU_BUCKET_PUBLIC
from dian.settings import TEMP_DIR
from dian.settings import DEBUG

from wechat_sdk.basic import WechatBasic

from dian.utils import get_md5
from wechat.models import WechatStore

import logging
logger = logging.getLogger('dian')


"""
认证相关
"""

def create_jsapi_signature(timestamp, nonceStr, url):
    """
    创建jsapi_signature
    """
    jsapi_ticket = _get_jsapi_ticket()
    wechat = WechatBasic(appid=APP_ID, appsecret=APP_SECRET,\
            jsapi_ticket=jsapi_ticket)
    signature = wechat.generate_jsapi_signature(timestamp, nonceStr, url,\
            jsapi_ticket)

    return signature


def _get_jsapi_ticket():
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
        access_token_expires_at.value = token_res.get('expires_in',\
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
        access_token_expires_at.value = res['expires_in']
        access_token_expires_at.save()
        access_token.value = res['access_token']
        access_token.save()

    return access_token.value


def get_auth_url_without_confirm(path, state=""):
    """
    获取微信授权的url，无用户确认提示
    """
    scope = "snsapi_base"
    return _make_auth_url(path, scope, state)


def get_auth_url_with_confirm(path, state=""):
    """
    获取微信授权的url，需用户确认：公众号获取个人信息
    """
    scope = "snsapi_userinfo"
    return _make_auth_url(path, scope, state)


def _make_auth_url(path, scope="snsapi_base", state="", domain=WP_DOMAIN):
    """
    获取微信网页授权url

    path: 跳转的路径 
    scope: snsapi_base:不弹出授权页面, snsapi_userinfo:弹出授权页面
    state: 认证后跳转携带的state参数
    domain: 跳转的域名
    """

    # redirect_uri: 认证后跳转url
    redirect_uri = urllib.quote_plus("%s%s" % (domain, path))

    url = "https://open.weixin.qq.com/connect/oauth2/authorize?\
appid=%(appid)s\
&redirect_uri=%(redirect_uri)s\
&response_type=code\
&scope=%(scope)s\
&state=%(state)s\
#wechat_redirect"
    params = {
            "appid": APP_ID,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
            }
    return url % params


"""
菜单相关
"""

def update_menu():
    """
    目前仅用作在pyhton shell中调用
    """
    wechat = WechatBasic(appid=APP_ID, appsecret=APP_SECRET)
    logger.info(wechat.get_menu())
    # 删除当前菜单
    wechat.delete_menu()
    # 创建菜单
    wechat.create_menu({
    'button':[
        {
            'type': 'view',
            'name': u'排队',
            'url': get_auth_url_with_confirm('#/queue'),
        },
        {
            'type': 'view',
            'name': u'点菜',
            'url': get_auth_url_with_confirm('#/menu'),
        },
        {
            'type': 'view',
            'name': u'图片',
            'url': get_auth_url_with_confirm('#/photo/index'),
        },
        # {
        #     'name': '菜单',
        #     'sub_button': [
        #         {
        #             'type': 'view',
        #             'name': '视频',
        #             'url': 'http://v.qq.com/'
        #         },
        #         {
        #             'type': 'click',
        #             'name': '赞一下我们',
        #             'key': 'V1001_GOOD'
        #         }
        #     ]
        # }
    ]})


"""
消息相关
"""

def send_article_message(openid, articles):
    """
    给微信用户发送链接类的客服消息
    """
    wechat = WechatBasic(appid=APP_ID, appsecret=APP_SECRET)
    wechat.send_article_message(openid, articles)


