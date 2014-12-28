#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import generics
from .serializers import TableSerializer, TableTypeSerializer
from .models import Table, TableType


class TableTypeList(generics.ListCreateAPIView):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer


class TableTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer

    def get_serializer(self, instance=None, data=None, files=None, many=False,
                       partial=False, allow_add_remove=False):
        if self.request.method == 'PUT':
            return TableTypeSerializer(instance=instance, data=data, many=many, partial=True)
        else:
            return TableTypeSerializer(instance=instance, data=data, many=many, partial=partial)


class TableList(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def get_serializer(self, instance=None, data=None, files=None, many=False,
                       partial=False, allow_add_remove=False):
        if self.request.method == 'PUT':
            return TableSerializer(instance=instance, data=data, many=many, partial=True)
        else:
            return TableSerializer(instance=instance, data=data, many=many, partial=partial)


