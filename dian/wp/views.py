#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

import requests
import urllib
import qrcode
import qiniu
import os
import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes 

from dian.settings import APP_ID, APP_SECRET
from dian.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY
from dian.settings import QINIU_BUCKET_PUBLIC
from dian.settings import QINIU_DOMAIN
from dian.settings import TEMP_DIR
from dian.settings import DEBUG
from dian.settings import API_DOMAIN
from dian.settings import WP_DOMAIN

from dian.utils import get_md5
from dian.utils import restaurant_required

from account.models import Member
from account.serializers import MemberSerializer

from restaurant.models import Restaurant
from registration.serializers import RegistrationSerializer


@api_view(['GET'])
@restaurant_required
def get_register_qrcode(request):
    """
    获取微信取号的二维码
    curl -X GET http://diankuai.cn:8000/wp/register-qrcode/ -H 'Authorization: Token f1b8ca936511301204fe627e63d502fc955fab8b' -H 'X-Restaurant-Id: 1'
    """
    redirect_uri = "%sregister/" % WP_DOMAIN
    print redirect_uri
    url = _make_web_auth_url(redirect_uri, request.current_restaurant.openid)
    localfile = _generate_qr_code(url)
    file_key = _upload_to_qiniu(localfile)
    return Response({
        "file_key": file_key
    })


def _make_web_auth_url(redirect_uri, state=""):
    """
    获取网页授权url

    redirect_uri: 认证后跳转url
    state: 认证后跳转携带的state参数
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
            "scope": "snsapi_userinfo",     # snsapi_base:不弹出授权页面, snsapi_userinfo:弹出授权页面
            "state": state,
            }
    return url % params


def _generate_qr_code(url):
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


def _upload_to_qiniu(localfile, clean_localfile=True):
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


# @csrf_protect
# def unuse_register(request, restaurant_openid):
#     """
#     微信取号页面
#     :param code: 微信提供的用来获取access_token的code
#     :param state: 用户授权未通过时，只有state
#     :param restaurant_openid: 餐厅的openid
#     """
#     code = request.GET.get('code', None)
#     state = request.GET.get('state', None)
# 
#     if DEBUG:
#         member = Member.objects.all()[0]
#         restaurant = Restaurant.objects.get(openid=restaurant_openid)
#         table_types = restaurant.table_types.order_by('id')
#         
#     else:
#         if not code:
#             return render_to_response('error.html')
# 
#         # 获取access token
#         access_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
#         access_params = {
#                 "appid": APP_ID,
#                 "secret": APP_SECRET,
#                 "code": code,
#                 "grant_type": "authorization_code"
#                 }
#         access_r = requests.get(access_url, params=access_params)
# 
#         openid = access_r.json().get('openid', None)
#         access_token = access_r.json().get('access_token', None)
# 
#         # 创建会员记录
#         if openid:
#             member = Member.objects.get_or_create(wp_openid=openid)[0]
# 
#             # 获取微信会员信息
#             userinfo_url = "https://api.weixin.qq.com/sns/userinfo"
#             userinfo_params = {
#                     "access_token": access_token,
#                     "openid": openid,
#                     "lang": "zh_CN"
#                     }
#             userinfo_r = requests.get(userinfo_url, params=userinfo_params)
#             member.wp_nickname = userinfo_r.json().get('nickname', '').encode('iso-8859-1').decode('utf-8')
#             member.wp_sex = userinfo_r.json().get('sex', None)
#             member.wp_province = userinfo_r.json().get('province', '').encode('iso-8859-1').decode('utf-8')
#             member.wp_city = userinfo_r.json().get('city', '').encode('iso-8859-1').decode('utf-8')
#             member.wp_country = userinfo_r.json().get('country', '').encode('iso-8859-1').decode('utf-8')
#             member.wp_headimgurl = userinfo_r.json().get('headimgurl', None)
#             member.wp_privilege = userinfo_r.json().get('privilege', None)
#             member.save()
#         else:
#             return render_to_response('error.html')
# 
#         restaurant = Restaurant.objects.get(openid=restaurant_openid)
#         table_types = restaurant.table_types.order_by('id')
# 
#     # 渲染模板
#     params = {
#             "member_id": member.id,
#             "table_types": table_types,
#             "restaurant_openid": restaurant_openid,
#             "restaurant_name": restaurant.name,
#             # "qrcode_path": "%s%s" % (QINIU_DOMAIN, key)
#             }
#     return render_to_response('register.html', RequestContext(request, params))
# 
# 
# def unuse_confirm_table_type(request):
#     """
#     选择餐桌，及确认取号
#     """
#     restaurant_openid = request.POST.get('restaurant_openid', None)
#     member_id = request.POST.get('member_id', None)
#     table_type = request.POST.get('table_type', None)
# 
#     member = Member.objects.get(id=member_id)
# 
#     data = request.POST.copy()
#     serializer = RegistrationSerializer(data=data)
# 
#     if serializer.is_valid():
#         obj = serializer.save(force_insert=True)
#         queue_number = obj.table_type.next_queue_number
#         obj.queue_number = queue_number
#         obj.create_time = datetime.datetime.now()
#         obj.table_min_seats = obj.table_type.min_seats
#         obj.table_max_seats = obj.table_type.max_seats
#         obj.queue_name = obj.table_type.name
#         obj.restaurant = obj.table_type.restaurant
#         obj.member = member
# 
#         # 取号方式：微信
#         obj.reg_method = 1 
# 
#         obj.save()
# 
#         # 让餐桌的拍号+1
#         obj.table_type.next_queue_number += 1
#         obj.table_type.save()
# 
#         params = {
#             "queue_name": obj.queue_name,
#             "queue_number": obj.queue_number,
#             "waiting_count": obj.table_type.get_registration_left
#                 }
#         return render_to_response('register_success.html',\
#                 RequestContext(request, params))
#     else:
#         return render_to_response('error.html')
