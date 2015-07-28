#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

import logging
logger = logging.getLogger('dian')


@api_view(['GET', 'POST'])
@authentication_classes(())
@permission_classes(())
def receive_message(request):
    """
    收取微信消息
    """
    if request.method == 'GET':
        logger.debug(int(request.GET.get('echostr')))
        return Response(int(request.GET.get('echostr')))
    elif request.method == 'POST':
        logger.debug('====================')
        logger.debug(request.body)
        return Response(int(request.GET.get('echostr')))


