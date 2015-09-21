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
from restaurant.utils import restaurant_required

from restaurant.models import Restaurant
from table.models import TableType

from account.models import Member
from account.serializers import MemberSerializer

from registration.models import Registration
from registration.models import REG_METHOD_WECHAT
from registration.serializers import RegistrationSerializer
from registration.serializers import RegistrationDetailSerializer

from registration.models import REGISTRATION_STATUS_WAITING
from registration.models import REGISTRATION_STATUS_REPAST
from registration.models import REGISTRATION_STATUS_EXPIRED

from registration.models import REGISTRATION_STATUS_WAITING


import logging
logger = logging.getLogger('dian')


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def confirm_table_type(request):
    """
    选择餐桌，及确认取号
    ---
    request_serializer: RegistrationSerializer

    parameters:
        - name: restaurant_openid
          type: string
          paramType: form
          required: true
        - name: table_type_id
          type: string
          paramType: form
          required: true

    responseMessages:
        - code: 400
          message: Field Error
        - code: 400
          message: Parameter Error(can not get member)

    """

    member = request.member
    if not member:
        return Response('Parameter Error(can not get member)',\
                status.HTTP_400_BAD_REQUEST)

    restaurant_openid = request.DATA.get('restaurant_openid')
    table_type_id = request.DATA.get('table_type_id')

    try:
        restaurant = Restaurant.objects.get(openid=restaurant_openid)
    except Restaurant.DoesNotExist:
        return Response('restaurant not found', status=status.HTTP_404_NOT_FOUND)

    try:
        restaurant = Restaurant.objects.get(openid=restaurant_openid)
    except Restaurant.DoesNotExist:
        return Response('restaurant not found', status=status.HTTP_404_NOT_FOUND)

    try:
        table_type = TableType.objects.get(pk=table_type_id)
    except TableType.DoesNotExist:
        return Response('table type not found', status=status.HTTP_404_NOT_FOUND)

    data = {
        'restaurant': restaurant.pk,
        'member': member.pk,
        'queue_name': table_type.name,
        'queue_number': table_type.next_queue_number,
        'table_min_seats': table_type.min_seats,
        'table_max_seats': table_type.max_seats,
        'reg_method': REG_METHOD_WECHAT,
        'table_type': table_type.pk
    }
    serializer = RegistrationSerializer(data=data)

    if serializer.is_valid():
        obj = serializer.save()
        # 让餐桌的拍号+1
        obj.table_type.next_queue()

        res = {
            "id": obj.pk
            # "queue_name": obj.queue_name,
            # "queue_number": obj.queue_number,
            # "waiting_count": obj.table_type.get_registration_left()
        }
        return Response(res, status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def list_current_registration(request):
    """
    获取顾客当前进行中的排号
    ---
    serializer: RegistrationDetailSerializer

    responseMessages:
        - code: 400
          message: Parameter Error(can not get member)

    """
    member = request.member
    if not member:
        return Response('Parameter Error(can not get member)',\
                status.HTTP_400_BAD_REQUEST)

    registrationList = Registration.objects.filter(member=member,\
            status=REGISTRATION_STATUS_WAITING)
    serializer = RegistrationDetailSerializer(registrationList)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def list_current_registration_by_restaurant(request):
    """
    获取顾客在当前餐厅的排号
    ---
    serializer: RegistrationDetailSerializer

    parameters:
        - name: restaurant_openid
          type: string
          paramType: form
          required: true

    responseMessages:
        - code: 400
          message: Parameter Error(can not get member)

    """
    member = request.member
    if not member:
        return Response('Parameter Error(can not get member)',\
                status.HTTP_400_BAD_REQUEST)

    restaurant_openid = request.GET.get('restaurant_openid', None)

    registrationList = Registration.objects.filter(member=member,\
            restaurant__openid=restaurant_openid, status=REGISTRATION_STATUS_WAITING)
    serializer = RegistrationDetailSerializer(registrationList)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def list_history_registration(request):
    """
    获取顾客的历史排号记录
    ---
    serializer: RegistrationDetailSerializer

    responseMessages:
        - code: 400
          message: Parameter Error(can not get member)

    """
    member = request.member
    if not member:
        return Response('Parameter Error(can not get member)',\
                status.HTTP_400_BAD_REQUEST)

    registrationList = Registration.objects.filter(member=member,\
            status__in=(REGISTRATION_STATUS_REPAST, REGISTRATION_STATUS_EXPIRED))
    serializer = RegistrationDetailSerializer(registrationList)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def get_detail_registration(request):
    """
    获取某一个排号的详情
    ---
    parameters:
        - name: id
          type: string
          paramType: query
          required: true

    serializer: RegistrationDetailSerializer

    responseMessages:
        - code: 400
          message: Parameter Error(can not get member)
        - code: 400
          message: Parameter Error(registration_id)
    """
    member = request.member
    if not member:
        return Response('Parameter Error(can not get member)',\
                status.HTTP_400_BAD_REQUEST)

    try:
        registration_id = request.GET.get('id', None)
        if not registration_id:
            raise Exception('registration id not in query')
        registration = Registration.objects.get(id=registration_id)
        serializer = RegistrationDetailSerializer(registration)
        return Response(serializer.data, status.HTTP_200_OK)
    except Exception, e:
        logger.error(e)
        return Response('Parameter Error(registration_id)',\
                status.HTTP_400_BAD_REQUEST)
