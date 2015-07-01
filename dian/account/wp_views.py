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
        # 返回会员信息
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # 通过code换取网页授权access_token
        access_res = _get_access_res(code)
        if access_res.get('errcode', None):
            return Response('code error', status=status.HTTP_400_BAD_REQUEST)
        openid = access_res.json().get('openid', None)
        access_token = access_res.json().get('access_token', None)

        # 获取或者创建会员对象
        member = Member.objects.get_or_create(wp_openid=openid)[0]

        # 授权类型为snsapi_userinfo
        # 通过access_token从微信中获取详细会员信息
        userinfo_res = _get_userinfo_res(openid, access_token)
        if not userinfo_res.get('errcode'):
            member.wp_nickname = userinfo_res.json().get('nickname', '').encode('iso-8859-1').decode('utf-8')
            member.wp_sex = userinfo_res.json().get('sex', None)
            member.wp_province = userinfo_res.json().get('province', '').encode('iso-8859-1').decode('utf-8')
            member.wp_city = userinfo_res.json().get('city', '').encode('iso-8859-1').decode('utf-8')
            member.wp_country = userinfo_res.json().get('country', '').encode('iso-8859-1').decode('utf-8')
            member.wp_headimgurl = userinfo_res.json().get('headimgurl', None)
            member.wp_privilege = userinfo_res.json().get('privilege', None)
            member.save()

        # 返回会员信息
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)


def _get_access_res(code):
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


def _get_userinfo_res(openid, access_token):
    userinfo_url = "https://api.weixin.qq.com/sns/userinfo"
    userinfo_params = {
            "access_token": access_token,
            "openid": openid,
            "lang": "zh_CN"
            }
    userinfo_res = requests.get(userinfo_url, params=userinfo_params)
    return userinfo_res

