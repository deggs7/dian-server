#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from account.models import User
from .utils import is_verified
from .tasks import create_and_send_captcha


@api_view(["POST"])
@permission_classes((AllowAny, ))
def captcha(request):
    """
    生成或者生成验证码
    """
    data = request.DATA.copy()
    phone = data.get('phone', None)
    captcha = data.get('captcha', None)

    if not phone or not User.objects.filter(username=phone).exists():
        return Response({"error": "不存在该用户"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(username=phone)

    if not captcha:
        # create captcha
        create_and_send_captcha(user)
        return Response(None, status.HTTP_200_OK)
    else:
        # verify captcha
        if not is_verified(captcha, user.username):
            return Response({"error": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(None, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny, ))
def reset_passwd(request):
    """
    根据用户输入重置密码，其中需要带上用户手机号与验证码
    """
    data = request.DATA.copy()
    phone = data.get('phone', None)
    captcha = data.get('captcha', None)
    new_password1 = data.get('new_password1', None)
    new_password2 = data.get('new_password2', None)

    user = User.objects.get(username=phone)

    if not phone or not user:
        return Response({"error": "不存在该用户"}, status=status.HTTP_400_BAD_REQUEST)

    if not captcha or not is_verified(captcha, user.username):
        return Response({"error": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)

    if not new_password1 or new_password1 != new_password2:
        return Response({"error": "密码错误"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password1)
    user.save()

    return Response({"info": "change password done"}, status=status.HTTP_200_OK)









