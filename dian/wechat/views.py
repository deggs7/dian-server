#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage,\
VideoMessage, LinkMessage, LocationMessage, EventMessage 

from dian.utils import restaurant_required
from dian.settings import WECHAT_TOKEN
from wechat.utils import get_auth_url_with_confirm
from wechat.utils import send_article_message

import logging
logger = logging.getLogger('dian')


@api_view(['GET', 'POST'])
@authentication_classes(())
@permission_classes(())
def receive_message(request):
    """
    收取微信消息
    """
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')

    wechat = WechatBasic(token=WECHAT_TOKEN)

    """
    用于在微信配置响应服务器时的验证
    {u'nonce': [u'280474307'], u'timestamp': [u'1438015570'],\
    u'echostr': [u'3904558954066704850'],\
    u'signature': [u'cfbd4c33549370f85424415310449f44e962c5d7']}
    """
    if wechat.check_signature(signature=signature, timestamp=timestamp,\
            nonce=nonce):
        if request.method == 'GET':
            if echostr:
                return Response(int(echostr))
        elif request.method == 'POST':
            body = request.body
            try:
                wechat.parse_data(body)
                message = wechat.get_message()
                response = _reply_message(message, wechat)
                return Response(response)
            except Exception, e:
                logger.error(e)
    return Response('')


def _reply_message(message, wechat):
    """
    根据消息的类型，做相应的处理
    """
    response = None
    if isinstance(message, TextMessage):
        if message.content == u'链接':
            logger.info('进入链接')
            response = wechat.response_news([
                {
                    'title': u'第一条新闻标题',
                    'description': u'第一条新闻描述，这条新闻没有预览图',
                    'url': u'http://www.google.com.hk/',
                },
                {
                    'title': u'第二条新闻标题, 这条新闻无描述',
                    'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                    'url': u'http://www.github.com/',
                },
            ])
        elif message.content == u'link':
            logger.info('进入link')
            redirect_path = "register/"
            url = get_auth_url_with_confirm(redirect_path)
            response = wechat.response_news([
                {
                    'title': u'进入取号页面',
                    'description': u'需要用户确认获取信息',
                    'url': url,
                },
            ])
        elif message.content == u'other':
            logger.info('进入other')
            response = wechat.response_text(content=u'会有两条消息')
            logger.info(message.source)

            redirect_path = "#/queue/"
            url = get_auth_url_with_confirm(redirect_path)
            send_article_message(message.source, [
                {
                    'title': u'进入排队首页',
                    'description': u'需要用户确认获取信息',
                    'url': url,
                },
            ])
        else:
            response = wechat.response_text(content=u'文字信息')
    elif isinstance(message, VoiceMessage):
        response = wechat.response_text(content=u'语音信息')
    elif isinstance(message, ImageMessage):
        response = wechat.response_text(content=u'图片信息')
    elif isinstance(message, VideoMessage):
        response = wechat.response_text(content=u'视频信息')
    elif isinstance(message, LinkMessage):
        response = wechat.response_text(content=u'链接信息')
    elif isinstance(message, LocationMessage):
        response = wechat.response_text(content=u'地理位置信息')
    elif isinstance(message, EventMessage):  # 事件信息
        if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                response = wechat.response_text(content=u'用户尚未关注时的二维码扫描关注事件')
            else:
                response = wechat.response_text(content=u'普通关注事件')
        elif message.type == 'unsubscribe':
            response = wechat.response_text(content=u'取消关注事件')
        elif message.type == 'scan':
            response = wechat.response_text(content=u'用户已关注时的二维码扫描事件')
        elif message.type == 'location':
            response = wechat.response_text(content=u'上报地理位置事件')
        elif message.type == 'click':
            response = wechat.response_text(content=u'自定义菜单点击事件')
        elif message.type == 'view':
            response = wechat.response_text(content=u'自定义菜单跳转链接事件')
        elif message.type == 'templatesendjobfinish':
            response = wechat.response_text(content=u'模板消息事件')
    return response


@api_view(['GET'])
@restaurant_required
def get_qrcode_list(request):
    """
    获取餐厅部署用到的全部二维码，包括：餐厅排队二维码，餐桌二维码
    """
    restaurant = request.current_restaurant
