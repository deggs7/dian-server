#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from restaurant.models import Restaurant
from reward.models import Strategy
from reward.serializers import StrategyGetSerializer


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def get_reward_strategy_by_restaurant(request):
    """
    获取餐厅对应的类型的奖励策略
    ---
    parameters:
        - name: openid
          type: string
          paramType: query
          required: true
        - name: strategy_type
          type: string
          paramType: query
          required: true

    serializer: reward.serializers.StrategyGetSerializer

    responseMessages:
        - code: 400
          message: prama error
        - code: 404
          message: Not Found
        - code: 200
          message: OK
    """
    openid = request.GET.get('openid')
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('param error', status=status.HTTP_400_BAD_REQUEST)
    strategy_type = int(request.GET.get('strategy_type'))
    if not strategy_type in [value[0] for value in Strategy.STRATEGY_TYPE]:
        return Response('No Strategy Found', status=status.HTTP_404_NOT_FOUND)

    strategy = restaurant.strategies.filter(type=strategy_type).first()
    if not strategy:
        return Response(None, status=status.HTTP_404_NOT_FOUND)
    return Response(StrategyGetSerializer(instance=strategy).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def determine_reward(request):
    """
    判断用户是否获取奖励
    ---
    parameters:
        - name: openid
          type: string
          paramType: query
          required: true
        - name: strategy_type
          type: int
          paramType: form
          required: true
        - name: count
          type: int
          paramType: form
          required: true

    responseMessages:
        - code: 400
          message: Bad Request
        - code: 404
          message: Not Found
        - code: 200
          message: OK
    """
    openid = request.GET.get('openid')
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('param error', status=status.HTTP_400_BAD_REQUEST)

    data = request.DATA.copy()
    if 'strategy_type' not in data or 'count' not in data:
        return Response('post data error', status=status.HTTP_400_BAD_REQUEST)

    strategy = restaurant.strategies.filter(type=int(data['strategy_type'])).first()
    if not strategy:
        return Response("no strategy for type %d" % int(data['strategy_type']), status=status.HTTP_404_NOT_FOUND)

    # 判断是否达到获得优惠券的条件
    if int(data['count']) > strategy.count:
        # 生成优惠券
        return Response({"result": True, "coupon": None}, status=status.HTTP_200_OK)
    return Response({"result": False}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def list_coupons(request):
    """
    获取用户在指定餐厅中的所有未过期未使用优惠券
    ---
    parameters:
        - name: openid
          type: string
          paramType: query
          required: true
        - name: strategy_type
          type: int
          paramType: form
          required: true
        - name: count
          type: int
          paramType: form
          required: true

    responseMessages:
        - code: 400
          message: Bad Request
        - code: 404
          message: Not Found
        - code: 200
          message: OK
    """
    openid = request.GET.get('openid')
