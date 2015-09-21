#!/usr/bin/env python
#! -*- encoding:utf-8 -*-
from django.db import models

from account.models import User

# class MsgStatistics(models.Model):
#     """
#     记录每个用户
#     """
#     MSG_TYPE = (
#         ('registration_remind', 'Registration Remind'),
#         ('reset_password', 'Reset Password'),
#         ('strategy', 'Strategy Reward')
#     )
# 
#     id = models.AutoField(primary_key=True)
#     owner = models.ForeignKey(User, related_name="own_msg_statistics")
#     success = models.IntegerField(default=0)
#     fail = models.IntegerField(default=0)
# 
#     type = models.CharField(max_length=16, choices=MSG_TYPE, default=MSG_TYPE[0][0])


