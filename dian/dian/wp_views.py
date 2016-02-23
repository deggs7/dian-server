#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from table.models import Table
from menu.serializers import MenuDetailSerializer

from dian.settings import WP_LIST_LENGTH

@api_view(["GET"])
@authentication_classes(())
@permission_classes(())
def settings(request):
    """
    获取系统变量（比如：列表长度的最大限制等）
    ---
    responseMessages:
        - code: 200
    """
    rt = {
        'LIST_LENGTH': WP_LIST_LENGTH
    }
    return Response(rt, status.HTTP_200_OK)
