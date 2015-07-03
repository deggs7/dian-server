#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from trade.models import Cart
from trade.serializers import CartSerializer

from dian.utils import restaurant_required


@api_view(['GET'])
@restaurant_required
def get_cart_by_restaurant(request):
    """
    获取购物车
    每个顾客访问每个餐厅，都会有一个对应的cart实体
    如果还没有对应的实例，则创建一个再返回
    从request的member（还未实现）中获取顾客信息
    ---
        serializer: trade.serializers.CartSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 201
              message: Created
            - code: 400
              message: Bad Request
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)
