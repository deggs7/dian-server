#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RestaurantSerializer, TableSerializer, TableTypeSerializer
from .models import Table, TableType
from registration.utils import get_next_registration
from registration.serializers import RegistrationSerializer


@api_view(["GET"])
def get_default_restaurant(request):
    restaurants = request.user.own_restaurants.all()
    if restaurants:
        default = restaurants[0]
        serializer = RestaurantSerializer(default)
        return Response(serializer.data)
    else:
        return Response('0 restaurants found', status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def create_restaurant(request):
    data = request.DATA.copy()
    data["owner"] = request.user.pk
    serializer = RestaurantSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            # 对老的registration的处理
            try:
                old_registration = self.object.registration
                old_registration.table = None
                old_registration.expire = True
                old_registration.save()
            except:
                pass

            registration = get_next_registration(self.object.table_type)
            if not registration:
                serializer.data['registration'] = None
                self.object.status = 'idle'
                self.object.save()
            else:
                serializer.data['registration'] = registration.id
                registration.table = self.object
                registration.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def table_type_registration(request):
    table_types = TableType.objects.all()
    ret = []
    for ttype in table_types:
        reg = ttype.registrations.exclude(table=None).filter(expire=False)
        if reg:
            reg = reg[0]
            serialzer = RegistrationSerializer(reg)
            ret.append({'id': ttype.id,
                        'name': ttype.name,
                        'table_number': reg.table.table_number,
                        'registration': serialzer.data,
                       })
        else:
            ret.append({'id': ttype.id,
                        'name': ttype.name,
                        'table_number': None,
                        'registration': None})

    return Response(ret)
