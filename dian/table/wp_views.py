#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes 

from restaurant.models import Restaurant
from table.models import TableType
from table.serializers import TableTypeSerializer


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def list_table_type_by_restaurant(request):
    """
    根据餐厅的openid，获取餐厅的所有table_type
    ---
        serializer: table.serializers.TableTypeSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
            - code: 400
              message: prama error
    """
    openid = request.GET.get('openid')
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('param error', status=status.HTTP_400_BAD_REQUEST)
    serializer = TableTypeSerializer(restaurant.table_types.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

