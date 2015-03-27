#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import requests
import urllib
import qrcode
import qiniu
import os
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from dian.settings import APP_ID, APP_SECRET
from dian.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY
from dian.settings import QINIU_BUCKET_PUBLIC
from dian.settings import QINIU_DOMAIN
from dian.settings import TEMP_DIR

from dian.utils import get_md5
from dian.utils import restaurant_required

from account.models import Member
from restaurant.models import Restaurant


def register(request, restaurant_openid):
    """
    微信取号页面
    :param code: 微信提供的用来获取access_token的code
    :param state: 用户授权未通过时，只有state
    :param restaurant_openid: 餐厅的openid
    """
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)

    if not code:
        return render_to_response('error.html')

    # 获取access token
    access_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    access_params = {
            "appid": APP_ID,
            "secret": APP_SECRET,
            "code": code,
            "grant_type": "authorization_code"
            }
    access_r = requests.get(access_url, params=access_params)

    openid = access_r.json().get('openid', None)
    access_token = access_r.json().get('access_token', None)

    # 创建会员记录
    if openid:
        member = Member.objects.get_or_create(wp_openid=openid)[0]
    else:
        return render_to_response('error.html')

    # 获取微信会员信息
    if False:
        userinfo_url = "https://api.weixin.qq.com/sns/userinfo"
        userinfo_params = {
                "access_token": access_token,
                "openid": openid,
                "lang": "zh_CN"
                }
        userinfo_r = requests.get(userinfo_url, params=userinfo_params)

    restaurant = Restaurant.objects.get(openid=restaurant_openid)
    table_types = restaurant.table_types.order_by('id')

    # 渲染模板
    params = {
            "member": member.id,
            "table_types": table_types,
            "restaurant_openid": restaurant_openid,
            # "qrcode_path": "%s%s" % (QINIU_DOMAIN, key)
            }
    return render_to_response('register.html', params)


@api_view(['GET'])
@restaurant_required
def get_register_qrcode(request):
    """
    获取微信取号的二维码
    """
    redirect_uri = "http://diankuai.cn:8000/wp/%s/register" %\
    request.current_restaurant.openid
    url = make_web_auth_url(redirect_uri)
    localfile = generate_qr_code(url)
    file_key = upload_to_qiniu(localfile)
    return Response({
        "file_key": file_key
    })


def make_web_auth_url(redirect_uri):
    """
    获取网页授权url
    """
    redirect_uri = urllib.quote_plus(redirect_uri)
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
            "scope": "snsapi_base",     # snsapi_base:不弹出授权页面, snsapi_userinfo:弹出授权页面
            "state": "",
            }
    return url % params


def generate_qr_code(url):
    """
    根据链接生成二维码，并返回二维码文件临时路径
    二维码上传后，应删除返回的临时文件，比如: os.remove(path)
    ref: https://pypi.python.org/pypi/qrcode
    """

    file_key = get_md5("%s%s" % (url,\
        datetime.datetime.now()))
    path = "%s%s" % (TEMP_DIR, file_key)

    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=4,
            )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    img.save(path)

    return path


def upload_to_qiniu(localfile, clean_localfile=True):
    """
    上传一个本地文件到七牛，返回文件的file_key，同时默认删除本地文件
    ref: http://developer.qiniu.com/docs/v6/sdk/python-sdk.html#upload-do
    """

    auth = qiniu.Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    file_key = get_md5("%s%s" % ("web_auth-%d" % 1,\
        datetime.datetime.now()))
    uptoken = auth.upload_token(bucket=QINIU_BUCKET_PUBLIC)

    mime_type = "text/plain"    # 二进制流 "application/octet-stream"
    ret, info = qiniu.put_file(uptoken, file_key, localfile, mime_type=mime_type)

    if ret is not None:
        if clean_localfile:
            # 默认上传成功会删除本地文件
            os.remove(localfile)
        return file_key
    else:
        # print(info) # error message in info
        return None

