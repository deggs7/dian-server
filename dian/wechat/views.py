#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

import logging
logger = logging.getLogger('dian')


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def receive_message(request):
    """
    收取微信消息
    """

    logger.debug(request.DATA)
    # import pdb; pdb.set_trace()
    
    return Response('hello')
