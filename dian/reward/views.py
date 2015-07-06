#!/usr/bin/env python
#! -*- encoding:utf-8 -*-


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reward.serializers import StrategySerializer

from dian.utils import restaurant_required


@api_view(['GET'])
@restaurant_required
def list_strategy(request):
    serializer = StrategySerializer(request.current_restaurant.strategies.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
