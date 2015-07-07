#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime
import qiniu
import time

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes 

from dian.settings import APP_ID, APP_SECRET
from dian.settings import DEBUG
from dian.settings import MD5_SEED

from dian.utils import get_md5
from wechat.utils import create_jsapi_signature


@api_view(["POST"])
@authentication_classes(())
@permission_classes(())
def get_jsapi_signature(request):
    """
    获取wechat-js-sdk使用权限的签名
    ---
    parameters:
        - name: url
          type: string
          paramType: form
          required: true

    type:
        appId:
            required: true
            type: string
        timestamp:
            required: true
            type: string
        nonceStr:
            required: true
            type: string
        signature:
            required: true
            type: string

    responseMessages:
        - code: 400
          message: Url Error
    """
    url = request.POST.get('url', None)
    if url:
        return Response(_generate_jsapi_signature_body(url))
    else:
        return Response('Url Error', status=status.HTTP_400_BAD_REQUEST)


def _generate_jsapi_signature_body(url):
    """
    准备生成签名需要的参数，并调用生成签名的函数，返回签名需要的字典
    """
    timestamp = int(time.time())
    nonceStr = get_md5("%s%s%s" % (datetime.datetime.now(), MD5_SEED, url))
    rt = {
        "appId": APP_ID,
        "timestamp": timestamp,
        "nonceStr": nonceStr,
        "signature": create_jsapi_signature(timestamp, nonceStr, url)
    }
    return rt
