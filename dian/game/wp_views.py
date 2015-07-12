#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime
import qiniu

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes 

from game.models import Game
from game.serializers import GameSerializer


@api_view(["GET"])
@authentication_classes(())
@permission_classes(())
def list_game_by_restaurant(request):
    """
    获取游戏列表（列表中包含餐厅的详细信息），需指定餐厅openid
    ---

    serializer: GameSerializer

    parameters:
        - name: openid
          type: string
          paramType: query
          required: true

    responseMessages:
        - code: 400
          message: Parameter Error(can not get restaurant openid)
        - code: 400
          message: Parameter Error(can not get member)

    """

    openid = request.GET.get('openid', None)
    score = 85
    """
    TODO: 向奖励模块获取餐厅游戏的奖励分数，用来乘以游戏系数
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('restaurant not found', status=status.HTTP_404_NOT_FOUND)
    """

    game_list = Game.objects.all()

    for game in game_list:
        game.score = int(score * game.ratio)
    serializer = GameSerializer(game_list)
    return Response(serializer.data, status.HTTP_200_OK)

