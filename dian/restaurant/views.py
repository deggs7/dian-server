#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime
import qiniu

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from restaurant.models import Restaurant

from restaurant.serializers import RestaurantSerializer

from dian.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY
from dian.settings import QINIU_BUCKET_PUBLIC
from dian.settings import WP_DOMAIN

from dian.utils import get_md5
from dian.utils import restaurant_required

from restaurant.utils import generate_qr_code
from restaurant.utils import upload_to_qiniu
from wechat.utils import get_auth_url_with_confirm


@api_view(["GET"])
def get_default_restaurant(request):
    restaurants = request.user.own_restaurants.all()
    if restaurants:
        default = restaurants[0]
        serializer = RestaurantSerializer(default)
        return Response(serializer.data)
    else:
        return Response('0 restaurants found', status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def uptoken_default_restaurant(request):
    restaurants = request.user.own_restaurants.all()
    if restaurants:
        default = restaurants[0]
        auth = qiniu.Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
        file_key = get_md5("%s%s" % ("restaurant-%d" % default.id,\
            datetime.datetime.now()))
        uptoken = auth.upload_token(bucket=QINIU_BUCKET_PUBLIC, key=file_key)
        return Response({
            "uptoken": uptoken,
            "file_key": file_key
        })

    return Response('no default restaurant', status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_restaurant(request):
    data = request.DATA.copy()
    data["owner"] = request.user.pk
    serializer = RestaurantSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_restaurant(request):
    data = request.DATA.copy()
    try:
        restaurant = Restaurant.objects.get(pk=data.get("restaurant_id"))
    except Restaurant.DoesNotExist:
        return Response('restaurant not found', status=status.HTTP_404_NOT_FOUND)
    serializer = RestaurantSerializer(restaurant, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@restaurant_required
def get_register_qrcode(request):
    """
    获取微信取号的二维码
    curl -X GET http://diankuai.cn:8000/wp/register-qrcode/ -H 'Authorization: Token f1b8ca936511301204fe627e63d502fc955fab8b' -H 'X-Restaurant-Id: 1'
    """
    redirect_path = "pages/register/"
    url = get_auth_url_with_confirm(redirect_path, request.current_restaurant.openid)
    localfile = generate_qr_code(url)
    file_key = upload_to_qiniu(localfile)
    return Response({
        "file_key": file_key
    })

