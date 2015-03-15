#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime

from django.db.models import Max
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dian.tasks import send_registration_remind
from .serializers import RegistrationSerializer
from .models import Registration


class RegistrationList(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            obj = serializer.save(force_insert=True)
            # 获取可用的queue_number号
            # queue_number = obj.table_type.registrations.aggregate(Max('queue_number'))['queue_number__max'] + 1
            queue_number = obj.table_type.next_queue_number
            obj.queue_number = queue_number
            obj.create_time = datetime.datetime.now()
            obj.table_min_seats = obj.table_type.min_seats
            obj.table_max_seats = obj.table_type.max_seats
            obj.restaurant = obj.table_type.restaurant
            obj.save()
            obj.table_type.next_queue_number += 1
            obj.table_type.save()

            # 发送短信给用户
            send_registration_remind(obj, 'getting')

            serializer.data['queue_number'] = queue_number
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_registration(request, pk):
    try:
        reg = Registration.objects.get(pk=pk)
    except Registration.DoesNotExist:
        return Response('registration not found', status=status.HTTP_404_NOT_FOUND)

    serializer = RegistrationSerializer(reg, data=request.DATA, partial=True)
    if serializer.is_valid():
        reg = serializer.save()
        status_action = request.DATA.get('status', None)
        if status_action == 'turn':
            reg.end_time = datetime.datetime.now()
            reg.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_msg_task(request):
    data = request.DATA.copy()
    registration_id = data.get('registration', None)
    msg_type = data.get('msg_type', None)
    if not registration_id:
        return Response({"error": "请指定序号"}, status=status.HTTP_400_BAD_REQUEST)
    if not msg_type:
        return Response({"error": "请指定短信类型"}, status=status.HTTP_400_BAD_REQUEST)

    registation = Registration.objects.get(pk=registration_id)
    send_registration_remind(registation, msg_type)
    return Response(None, status=status.HTTP_202_ACCEPTED)



