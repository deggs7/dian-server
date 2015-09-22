#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from table.models import Table
from menu.serializers import MenuDetailSerializer


@api_view(["GET"])
@authentication_classes(())
@permission_classes(())
def list_menu_by_table(request):
    """
    根据餐桌的openid，获取餐厅的所有menus
    ---
    serializer: menu.serializers.MenuDetailSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    openid = request.GET.get('openid')

    try:
        table = Table.objects.get(openid=openid)
    except Table.DoesNotExist:
        return Response('param error: no table found', status=status.HTTP_400_BAD_REQUEST)

    restaurant = table.restaurant

    serializer = MenuDetailSerializer(restaurant.menus.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
