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

from dian.utils import get_md5
from dian.utils import restaurant_required

from account.models import Member
from account.serializers import MemberSerializer

from restaurant.models import Restaurant
from registration.serializers import RegistrationSerializer


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def confirm_table_type(request):
    """
    选择餐桌，及确认取号
    """
    restaurant_openid = request.POST.get('restaurant_openid', None)
    wp_openid = request.POST.get('wp_openid', None)
    table_type = request.POST.get('table_type', None)

    member = Member.objects.get(wp_openid=wp_openid)

    data = request.POST.copy()
    serializer = RegistrationSerializer(data=data)

    if serializer.is_valid():
        obj = serializer.save(force_insert=True)
        queue_number = obj.table_type.next_queue_number
        obj.queue_number = queue_number
        obj.create_time = datetime.datetime.now()
        obj.table_min_seats = obj.table_type.min_seats
        obj.table_max_seats = obj.table_type.max_seats
        obj.queue_name = obj.table_type.name
        obj.restaurant = obj.table_type.restaurant
        obj.member = member

        # 取号方式：微信
        obj.reg_method = 1 

        obj.save()

        # 让餐桌的拍号+1
        obj.table_type.next_queue_number += 1
        obj.table_type.save()

        res = {
            "queue_name": obj.queue_name,
            "queue_number": obj.queue_number,
            "waiting_count": obj.table_type.get_registration_left()
                }
        return Response(res, status.HTTP_200_OK)
    else:
        return Response('register error', status.HTTP_400_BAD_REQUEST)


def _get_access_res(code):
    """
    通过code换取网页授权access_token
    """
    # 获取access token
    access_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    access_params = {
            "appid": APP_ID,
            "secret": APP_SECRET,
            "code": code,
            "grant_type": "authorization_code"
            }
    access_res = requests.get(access_url, params=access_params)
    return access_res


def _get_userinfo_res(openid, access_token):
    userinfo_url = "https://api.weixin.qq.com/sns/userinfo"
    userinfo_params = {
            "access_token": access_token,
            "openid": openid,
            "lang": "zh_CN"
            }
    userinfo_res = requests.get(userinfo_url, params=userinfo_params)
    return userinfo_res

