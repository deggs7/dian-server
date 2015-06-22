#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime
import qiniu

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes 

from restaurant.models import Restaurant

from restaurant.serializers import RestaurantSerializer

from dian.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY
from dian.settings import QINIU_BUCKET_PUBLIC
from dian.utils import get_md5


@api_view(["GET"])
@authentication_classes(())
@permission_classes(())
def get_restaurant(request):
    """
    通过openid获取餐厅信息
    """

    openid = request.GET.get('openid', None)
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('restaurant not found', status=status.HTTP_404_NOT_FOUND)
    serializer = RestaurantSerializer(restaurant)
    return Response(serializer.data)
