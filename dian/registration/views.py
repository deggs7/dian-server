#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime

from django.db.models import Max
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from registration.models import Registration
from registration.models import REG_METHOD_PHONE
from registration.serializers import RegistrationSerializer
from registration.serializers import RegistrationHistorySerializer

from account.models import Member

from table.models import TableType

from message.utils import render_join
from message.tasks import send_sms

from registration.models import REGISTRATION_STATUS_WAITING
from registration.models import REGISTRATION_STATUS_REPAST
from registration.models import REGISTRATION_STATUS_EXPIRED

# from dian.tasks import send_registration_remind
from restaurant.utils import restaurant_required


import logging
logger = logging.getLogger('dian')


@api_view(['POST'])
def join_queue(request):
    """
    选择餐桌，及确认取号
    ---
    request_serializer: RegistrationSerializer

    parameters:
        - name: phone
          type: string
          paramType: form
          required: true
        - name: table_type_id
          type: string
          paramType: form
          required: true

    responseMessages:
        - code: 400
          message: Field Error
        - code: 400
          message: Parameter Error(can not get member)

    """

    restaurant = request.current_restaurant

    phone = request.DATA.get('phone')
    table_type_id = request.DATA.get('table_type_id')

    member = Member.objects.get_or_create(phone=phone)[0]

    try:
        table_type = TableType.objects.get(pk=table_type_id)
    except TableType.DoesNotExist:
        return Response('table type not found', status=status.HTTP_404_NOT_FOUND)

    data = {
        'restaurant': restaurant.pk,
        'member': member.pk,
        'queue_name': table_type.name,
        'queue_number': table_type.next_queue_number,
        'table_min_seats': table_type.min_seats,
        'table_max_seats': table_type.max_seats,
        'reg_method': REG_METHOD_PHONE,
        'table_type': table_type.pk
    }
    serializer = RegistrationSerializer(data=data)

    if serializer.is_valid():
        obj = serializer.save()
        # 让餐桌的拍号+1
        obj.table_type.next_queue()

        # 给顾客发送短信提醒
        content = render_join(restaurant.name, obj.queue_name, obj.queue_number,\
                (obj.table_type.get_registration_left() - 1))
        send_sms.delay(obj.member.phone, content)
        
        return Response(serializer.data, status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def make_repast(request, pk):
    """
    将号码状态改为就餐
    """
    try:
        reg = Registration.objects.get(pk=pk)
    except Registration.DoesNotExist:
        return Response('registration not found', status=status.HTTP_404_NOT_FOUND)
    data = {
        'status': REGISTRATION_STATUS_REPAST
    }
    serializer = RegistrationSerializer(reg, data=data, partial=True)
    if serializer.is_valid():
        reg = serializer.save()
        reg.end_time = datetime.datetime.now()
        reg.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def make_expired(request, pk):
    """
    将号码状态改为过号
    """
    try:
        reg = Registration.objects.get(pk=pk)
    except Registration.DoesNotExist:
        return Response('registration not found', status=status.HTTP_404_NOT_FOUND)
    data = {
        'status': REGISTRATION_STATUS_EXPIRED
    }
    serializer = RegistrationSerializer(reg, data=data, partial=True)
    if serializer.is_valid():
        reg = serializer.save()
        reg.end_time = datetime.datetime.now()
        reg.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for statistics report
@api_view(['POST'])
@restaurant_required
def get_daily_registration(request):
    from_days_ago = request.DATA.get('since_days', 14)
    regs = request.current_restaurant.registrations
    now_day = datetime.datetime.now().date()
    from_day = now_day - datetime.timedelta(days=from_days_ago)
    day = 0
    ret = []
    while day <= from_days_ago:
        reg_day = from_day + datetime.timedelta(days=day)
        reg_count = regs.filter(create_time__gte=reg_day,
                                create_time__lt=reg_day+datetime.timedelta(days=1)).count()
        ret.append({
            "date": "%d月%d日" % (reg_day.month, reg_day.day),
            "reg_count": reg_count
        })
        day += 1

    return Response(ret, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def get_avg_waiting_time(request):
    from_days_ago = request.DATA.get('since_days', 14)
    regs = request.current_restaurant.registrations
    now_day = datetime.datetime.now().date()
    from_day = now_day - datetime.timedelta(days=from_days_ago)
    day = 0
    ret = []
    while day <= from_days_ago:
        reg_day = from_day + datetime.timedelta(days=day)
        t_regs = regs.filter(create_time__gte=reg_day,
                             create_time__lte=reg_day+datetime.timedelta(days=1))

        t_repast_regs = t_regs.filter(status__exact=REGISTRATION_STATUS_REPAST, end_time__isnull=False)
        t_expired_regs = t_regs.filter(status__exact=REGISTRATION_STATUS_REPAST, end_time__isnull=False)

        avg_waitime_repast = sum([(reg.end_time - reg.create_time).seconds for reg in t_repast_regs]) / t_repast_regs.count() \
            if t_repast_regs.count() else 0
        avg_waitime_expired = sum([(reg.end_time - reg.create_time).seconds for reg in t_expired_regs]) / t_expired_regs.count() \
            if t_expired_regs.count() else 0

        ret.append({
            "date": "%d月%d日" % (reg_day.month, reg_day.day),
            "avg_repast_value": avg_waitime_repast,
            "avg_expired_value": avg_waitime_expired
        })
        day += 1

    return Response(ret, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def get_daily_type_registration(request):
    from_days_ago = request.DATA.get('since_days', 14)
    regs = request.current_restaurant.registrations
    now_day = datetime.datetime.now().date()
    from_day = now_day - datetime.timedelta(days=from_days_ago)
    day = 0
    ret = []
    while day <= from_days_ago:
        reg_day = from_day + datetime.timedelta(days=day)
        t_regs = regs.filter(create_time__gte=reg_day,
                             create_time__lt=reg_day+datetime.timedelta(days=1))
        t_repast_count = t_regs.filter(status__exact=REGISTRATION_STATUS_REPAST).count()
        t_expired_count = t_regs.filter(status__exact=REGISTRATION_STATUS_EXPIRED).count()

        ret.append({
            "date": "%d月%d日" % (reg_day.month, reg_day.day),
            "reg_repast_count": t_repast_count,
            "reg_expired_count": t_expired_count
        })
        day += 1

    return Response(ret, status=status.HTTP_200_OK)


# for history report
@api_view(['GET'])
@restaurant_required
def get_today_registration(request):
    ret = request.current_restaurant.registrations\
        .filter(status__in=[REGISTRATION_STATUS_REPAST,\
            REGISTRATION_STATUS_EXPIRED])\
        .order_by('-queue_number')[:20]
    serializer = RegistrationHistorySerializer(ret, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# class RegistrationList(generics.ListCreateAPIView):
#     """
#     不建议使用Django RESTful的这种方式
#     直接封装为针对业务的一个方法，替换此方法
#     """
#     queryset = Registration.objects.all()
#     serializer_class = RegistrationSerializer
# 
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.DATA, files=request.FILES)
# 
#         if serializer.is_valid():
#             obj = serializer.save(force_insert=True)
#             # 获取可用的queue_number号
#             # queue_number = obj.table_type.registrations.aggregate(Max('queue_number'))['queue_number__max'] + 1
#             queue_number = obj.table_type.next_queue_number
#             obj.queue_number = queue_number
#             obj.create_time = datetime.datetime.now()
#             obj.table_min_seats = obj.table_type.min_seats
#             obj.table_max_seats = obj.table_type.max_seats
#             obj.queue_name = obj.table_type.name
#             obj.restaurant = obj.table_type.restaurant
#             obj.save()
#             obj.table_type.next_queue_number += 1
#             obj.table_type.save()
# 
#             # 发送短信给用户
#             send_registration_remind(obj, 'getting')
# 
#             serializer.data['queue_number'] = queue_number
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED,
#                             headers=headers)
# 
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def update_registration(request, pk):
#     """
#     不建议提供update方法
#     后期应直接封装为针对业务的一个方法，替换此方法
#     """
#     try:
#         reg = Registration.objects.get(pk=pk)
#     except Registration.DoesNotExist:
#         return Response('registration not found', status=status.HTTP_404_NOT_FOUND)
# 
#     serializer = RegistrationSerializer(reg, data=request.DATA, partial=True)
#     if serializer.is_valid():
#         reg = serializer.save()
#         status_action = request.DATA.get('status', None)
#         if status_action == REGISTRATION_STATUS_WAITING:
#             reg.end_time = datetime.datetime.now()
#             reg.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


