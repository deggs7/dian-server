#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import TableSerializer, TableTypeSerializer
from .models import Table, TableType
from regstration.utils import get_next_regstration


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

    def put(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if self.object is None:
            self.object = serializer.save(force_insert=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.object = serializer.save(force_update=True)
        # 通过状态更改来判断是否叫号
        if request.DATA['status'] == 'waiting':
            # 对老的regstration的处理
            try:
                old_regstration = self.object.regstration
                old_regstration.table = None
                old_regstration.expire = True
                old_regstration.save()
            except:
                pass

            regstration = get_next_regstration(self.object.table_type)
            if not regstration:
                serializer.data['regstration'] = None
                self.object.status = 'idle'
                self.object.save()
            else:
                serializer.data['regstration'] = regstration.id
                regstration.table = self.object
                regstration.save()

        return Response(serializer.data, status=status.HTTP_200_OK)





