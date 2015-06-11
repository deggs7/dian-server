#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from trade.models import Cart
from trade.models import CartItem
from trade.models import Order
from trade.models import OrderItem

from trade.serializers import CartSerializer
from trade.serializers import CartItemSerializer
from trade.serializers import OrderSerializer
from trade.serializers import OrderItemSerializer

from dian.utils import restaurant_required


@api_view(['GET'])
@restaurant_required
def get_cart_by_restaurant(request, restaurant_pk):
    """
    (微信端方案还不确定，先不实现此接口)获取购物车
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


@api_view(['GET'])
@restaurant_required
def confirm_order(request, order_pk):
    """
    餐厅确认顾客提交的订单
    ---
        serializer: trade.serializers.OrderSerializer
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


@api_view(['GET'])
@restaurant_required
def reject_order(request, order_pk):
    """
    餐厅退回顾客提交的订单
    ---
        serializer: trade.serializers.OrderSerializer
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


@api_view(['GET'])
@restaurant_required
def finish_order(request, order_pk):
    """
    餐厅关闭已经确认过的订单(主要指顾客以及结账之后)
    ---
        serializer: trade.serializers.OrderSerializer
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



