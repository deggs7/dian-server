#!/usr/bin/env python
# -*- coding: utf-8 -*-

from account.models import Member
from dian.settings import DEBUG


class MemberMiddleware(object):

    def process_request(self, request):
        """
        从header中读出x_member_id(微信会员), 获取当前微信会员，放入request中。
        """

        member_id = request.META.get('HTTP_X_MEMBER_ID', None)
        if member_id:
            try:
                member = Member.objects.get(wp_openid=member_id)
                request.member = member
            except Member.DoesNotExist:
                request.member = None
        else:
            request.member = None

        # 用于辅助接口文档的呈现
        if DEBUG and not request.member:
            try:
                request.member = Member.objects.all()[0]
            except:
                request.member = None

        return
