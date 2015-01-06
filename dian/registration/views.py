#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from django.db.models import Max
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
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
            queue_number = obj.table_type.registrations.aggregate(Max('queue_number'))['queue_number__max'] + 1
            obj.queue_number = queue_number
            obj.save()

            serializer.data['queue_number'] = queue_number
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


