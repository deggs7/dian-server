#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
import datetime


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username,\
        email and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        # if not email:
        #     raise ValueError('Users must have an email')

        user = self.model(
            username=username,
            # email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username,\
        email and password.
        """
        user = self.create_user(
            username=username,
            # email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    点快中的管理员
    - 目前为餐厅的拥有者
    """
    username = models.CharField(
        verbose_name='Username',
        max_length=64,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    alias = models.CharField(max_length=400, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Member(models.Model):
    """
    会员实体
    - 通过短信或者微信取号的会员
    """

    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    # 用户是否订阅该公众号标识，值为0时，代表此用户没有关注该公众号，拉取不到其余信息。
    wp_subscribe = models.IntegerField(default=0)   
    # openid	微信的openid，用户的唯一标识
    wp_openid = models.CharField(max_length=255, null=True, blank=True)
    # nickname	用户昵称
    wp_nickname = models.CharField(max_length=255, null=True, blank=True)
    # sex	用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
    wp_sex = models.IntegerField(default=0)
    # city	普通用户个人资料填写的城市
    wp_city = models.CharField(max_length=255, null=True, blank=True)
    # country	国家，如中国为CN
    wp_country = models.CharField(max_length=255, null=True, blank=True)
    # province	用户个人资料填写的省份
    wp_province = models.CharField(max_length=255, null=True, blank=True)
    # language	用户的语言，简体中文为zh_CN
    wp_language = models.CharField(max_length=255, null=True, blank=True)
    # headimgurl	用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
    wp_headimgurl = models.CharField(max_length=255, null=True, blank=True)
    # subscribe_time	用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间
    wp_subscribe_time = models.CharField(max_length=255, null=True, blank=True)
    # unionid 只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。
    wp_unionid = models.CharField(max_length=255, null=True, blank=True)
    # remark	公众号运营者对粉丝的备注，公众号运营者可在微信公众平台用户管理界面对粉丝添加备注
    wp_remark = models.CharField(max_length=255, null=True, blank=True)
    # groupid	用户所在的分组ID
    wp_groupid = models.CharField(max_length=255, null=True, blank=True)


class SeedUser(models.Model):
    """
    申请开通服务的种子用户
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=1000, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=255, null=False, blank=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
