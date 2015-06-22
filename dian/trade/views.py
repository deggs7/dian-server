#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime

from trade.models import Order

from trade.serializers import OrderSerializer

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
            - code: 400
              message: Bad Request
            - code: 403
              message: Forbidden
            - code: 404
              message: Not Found
            - code: 401
              message: Not authenticated
    """
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response('order not found', status=status.HTTP_404_NOT_FOUND)

    if not order.restaurant or order.restaurant != request.current_restaurant:
        return Response('order forbidden', status.HTTP_403_FORBIDDEN)

    if order.status != Order.STATUS[0][0]:
        return Response('order error status', status.HTTP_400_BAD_REQUEST)

    order.status = Order.STATUS[1][0]
    order.confirm_time = datetime.datetime.now()
    order.save()
    serializer = OrderSerializer(data=order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def reject_order(request, order_pk):
    """
    餐厅退回顾客提交的订单(订单在已下单情况下才可以使用已退回功能)
    ---
        serializer: trade.serializers.OrderSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
            - code: 403
              message: Forbidden
            - code: 404
              message: Not Found
            - code: 401
              message: Not authenticated
    """
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response('order not found', status=status.HTTP_404_NOT_FOUND)

    if not order.restaurant or order.restaurant != request.current_restaurant:
        return Response('order forbidden', status.HTTP_403_FORBIDDEN)

    if order.status != Order.STATUS[0][0]:
        return Response('order error status', status.HTTP_400_BAD_REQUEST)

    order.status = Order.STATUS[3][0]
    order.save()
    serializer = OrderSerializer(data=order)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
            - code: 404
              message: Not Found
            - code: 401
              message: Not authenticated
    """
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response('order not found', status=status.HTTP_404_NOT_FOUND)

    if not order.restaurant or order.restaurant != request.current_restaurant:
        return Response('order forbidden', status.HTTP_403_FORBIDDEN)

    if order.status != Order.STATUS[1][0]:
        return Response('order error status', status.HTTP_400_BAD_REQUEST)

    order.status = Order.STATUS[2][0]
    order.pay_time = datetime.datetime.now()
    order.save()
    serializer = OrderSerializer(data=order)
    return Response(serializer.data, status=status.HTTP_200_OK)


