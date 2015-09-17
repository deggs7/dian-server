#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import requests

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes 

from dian.settings import APP_ID, APP_SECRET
from dian.settings import DEBUG

from account.models import Member
from account.serializers import MemberSerializer
from wechat.utils import get_access_token

import logging
logger = logging.getLogger('dian')


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def get_member(request):
    """
    根据微信redirect后的code，获取微信会员的wp_openid
    只有在关注后，或者以snsapi_userinfo方式授权后，才能获得详细用户信息

    :param code: 微信提供的用来获取access_token的code
    :param state: 用户授权未通过时，只有state，目前由前端判断
    """
    code = request.GET.get('code', None)

    if DEBUG:
        members = Member.objects.all()
        member = None
        if not members:
            member = Member.objects.get_or_create(wp_openid="test")[0]
        else:
            member = members[0]
        # 返回会员信息
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # 通过code换取网页授权access_token
        try:
            access_res = _get_access_res_for_web(code)
            if access_res.json().get('errcode', None):
                logger.error('error when get_openid:%s' %\
                        access_res.json().get('errmsg', None))
                return Response('code error', status=status.HTTP_400_BAD_REQUEST)
            openid = access_res.json().get('openid', None)
            # access_token = access_res.json().get('access_token', None)

            # basic_access_res = _get_access_res_for_basic()
            # access_token = basic_access_res.json().get('access_token', None)
            access_token = get_access_token()

            # 获取或者创建会员对象
            member = Member.objects.get_or_create(wp_openid=openid)[0]

            # 授权类型为snsapi_userinfo
            # 通过access_token从微信中获取详细会员信息
            userinfo = _get_userinfo_for_basic(openid, access_token)
            if userinfo:
                # member.wp_nickname = userinfo.get('nickname', '').encode('iso-8859-1').decode('utf-8')
                # member.wp_sex = userinfo.get('sex', None)
                # member.wp_province = userinfo.get('province', '').encode('iso-8859-1').decode('utf-8')
                # member.wp_city = userinfo.get('city', '').encode('iso-8859-1').decode('utf-8')
                # member.wp_country = userinfo.get('country', '').encode('iso-8859-1').decode('utf-8')
                # member.wp_headimgurl = userinfo.get('headimgurl', None)
                # member.wp_privilege = userinfo.get('privilege', None)
                member.wp_subscribe = userinfo.get('subscribe', '')
                member.wp_openid = userinfo.get('openid', '')
                member.wp_nickname = userinfo.get('nickname', '')
                member.wp_sex = userinfo.get('sex', None)
                member.wp_city = userinfo.get('city', '')
                member.wp_country = userinfo.get('country', '')
                member.wp_province = userinfo.get('province', '')
                member.wp_language = userinfo.get('language', '')
                member.wp_headimgurl = userinfo.get('headimgurl', None)
                member.wp_subscribe_time = userinfo.get('subscribe_time', None)
                member.wp_unionid = userinfo.get('unionid', None)
                member.wp_remark = userinfo.get('remark', None)
                member.wp_groupid = userinfo.get('groupid', None)
                member.save()

            # 返回会员信息
            serializer = MemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception,e:
            logger.error(e)
            return Response('param error: can not get member', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def get_member_by_openid(request):
    """
    根据微信openid获取member信息
    """
    openid = request.GET.get('openid', None)
    try:
        member = Member.objects.filter(wp_openid=openid)[0]
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception, e:
        rt = {
            'err_msg': e.message
        }
        return Response(rt, status=status.HTTP_400_BAD_REQUEST)


def _get_access_res_for_basic():
    """
    换取基础接口授权access_token
    """
    # 获取access token
    access_url = "https://api.weixin.qq.com/cgi-bin/token"
    access_params = {
            "appid": APP_ID,
            "secret": APP_SECRET,
            "grant_type": "client_credential"
            }
    access_res = requests.get(access_url, params=access_params)
    return access_res


def _get_access_res_for_web(code):
    """
    通过code换取网页授权access_token
    """
    # 获取access token
    access_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    access_params = {
            "appid": APP_ID,
            "secret": APP_SECRET,
            "code": code,
            "grant_type": "authorization_code"
            }
    access_res = requests.get(access_url, params=access_params)
    return access_res


def _get_userinfo_for_basic(openid, access_token):
    """
    基本接口中的获取用户信息
    http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
    此access_token通过以下方式获得
    http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html
    """
    url = "https://api.weixin.qq.com/cgi-bin/user/info"
    return _get_userinfo_res(openid, access_token, url)


def _get_userinfo_for_web(openid, access_token):
    """
    网页中获取用户信息
    此access_token通过以下方式中获得
    http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
    """
    url = "https://api.weixin.qq.com/sns/userinfo"
    return _get_userinfo_res(openid, access_token, url)


def _get_userinfo_res(openid, access_token, url):
    # userinfo_url = "https://api.weixin.qq.com/sns/userinfo"
    userinfo_params = {
            "access_token": access_token,
            "openid": openid,
            "lang": "zh_CN"
            }
    userinfo_res = requests.get(url, params=userinfo_params)
    if userinfo_res.json().get('errcode', None):
        logger.error(userinfo_res.json().get('errmsg'))
        return None
    else:
        return userinfo_res.json()


