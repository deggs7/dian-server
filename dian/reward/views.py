#!/usr/bin/env python
#! -*- encoding:utf-8 -*-


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reward.serializers import StrategySerializer, StrategyGetSerializer
from reward.serializers import RewardSerializer

from reward.models import Reward
from reward.models import Strategy

from dian.utils import restaurant_required


@api_view(['GET'])
@restaurant_required
def list_strategy(request):
    """
    列出餐厅所有的奖励策略
    ---
        serializer: reward.serializers.StrategySerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 403
              message: Forbidden
            - code: 404
              message: Not Found
            - code: 401
              message: Not authenticated
    """
    serializer = StrategyGetSerializer(request.current_restaurant.strategies.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def create_strategy(request):
    """
    生成奖励策略
    ---
        serializer: reward.serializers.StrategySerializer
        omit_serializer: false

        responseMessages:
            - code: 201
              message: Created
            - code: 400
              message: Bad Request
            - code: 401
              message: Not authenticated
    """
    data = request.DATA.copy()
    if type(data['reward']) == dict:
        data['reward'] = data['reward']['id']
    serializer = StrategySerializer(data=data)
    if serializer.is_valid():
        strategy = serializer.save()
        strategy.restaurant = request.current_restaurant
        strategy.save()
        return Response(StrategyGetSerializer(instance=strategy).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@restaurant_required
def update_strategy(request, pk):
    """
    更新奖励策略
    ---
        serializer: reward.serializers.StrategySerializer
        omit_serializer: false

        responseMessages:
            - code: 202
              message: Accepted
            - code: 400
              message: Bad Request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Not Found
    """
    try:
        strategy = Strategy.objects.get(pk=pk)
    except Strategy.DoesNotExist:
        return Response('strategy not found', status=status.HTTP_404_NOT_FOUND)

    data = request.DATA.copy()
    if type(data['reward']) == dict:
        data['reward'] = data['reward']['id']
    serializer = StrategySerializer(strategy, data=data, partial=True)
    if serializer.is_valid():
        strategy = serializer.save()
        return Response(StrategyGetSerializer(instance=strategy).data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@restaurant_required
def delete_strategy(request, pk):
    """
    删除奖励策略
    ---
        serializer: reward.serializers.StrategySerializer
        omit_serializer: false

        responseMessages:
            - code: 202
              message: Accepted
            - code: 401
              message: Not authenticated
            - code: 404
              message: Not Found
    """
    try:
        strategy = Strategy.objects.get(pk=pk)
    except Strategy.DoesNotExist:
        return Response('strategy not found', status=status.HTTP_404_NOT_FOUND)

    strategy.delete()
    return Response(None, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@restaurant_required
def list_reward(request):
    """
    列出餐厅所有的奖品
    ---
        serializer: reward.serializers.RewardSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 401
              message: Not authenticated
    """
    serializer = RewardSerializer(request.current_restaurant.rewards.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def create_reward(request):
    """
    生成奖品
    ---
        serializer: reward.serializers.RewardSerializer
        omit_serializer: false

        responseMessages:
            - code: 201
              message: Created
            - code: 400
              message: Bad Request
            - code: 401
              message: Not authenticated
    """
    data = request.DATA.copy()
    serializer = RewardSerializer(data=data)
    if serializer.is_valid():
        strategy = serializer.save()
        strategy.restaurant = request.current_restaurant
        strategy.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@restaurant_required
def update_reward(request, pk):
    """
    更新奖品
    ---
        serializer: reward.serializers.RewardSerializer
        omit_serializer: false

        responseMessages:
            - code: 202
              message: Accepted
            - code: 400
              message: Bad Request
            - code: 404
              message: Not Found
            - code: 401
              message: Not authenticated
    """
    try:
        reward = Reward.objects.get(pk=pk)
    except Strategy.DoesNotExist:
        return Response('reward not found', status=status.HTTP_404_NOT_FOUND)

    serializer = RewardSerializer(reward, data=request.DATA, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@restaurant_required
def delete_reward(request, pk):
    """
    删除奖品
    ---
        serializer: reward.serializers.RewardSerializer
        omit_serializer: false

        responseMessages:
            - code: 202
              message: Accepted
            - code: 401
              message: Not authenticated
            - code: 404
              message: Not Found
    """
    try:
        reward = Reward.objects.get(pk=pk)
    except Strategy.DoesNotExist:
        return Response('reward not found', status=status.HTTP_404_NOT_FOUND)

    reward.delete()
    return Response(None, status=status.HTTP_202_ACCEPTED)
