#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from functools import wraps

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RestaurantSerializer, TableSerializer, TableTypeSerializer
from .models import Table, TableType
from registration.utils import get_next_registration
from registration.serializers import RegistrationSerializer


def restaurant_required(func):
    @wraps(func)
    def decorated_view(request, *args, **kwargs):
        if not request.current_restaurant:
            return Response("No restaurant found", status=status.HTTP_400_BAD_REQUEST)
        if request.current_restaurant.owner != request.user:
            return Response("No authority to access this restaurant", status=status.HTTP_403_FORBIDDEN)

        return func(request, *args, **kwargs)

    return decorated_view


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


@api_view(['GET', 'POST'])
@restaurant_required
def list_or_create_table_type(request):
    if request.method == 'GET':
        serializer = TableTypeSerializer(request.current_restaurant.table_types.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.DATA.copy()
        serializer = TableTypeSerializer(data=data)
        if serializer.is_valid():
            table_type = serializer.save()
            table_type.restaurant = request.current_restaurant
            table_type.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@restaurant_required
def get_or_update_table_type(request, pk):
    try:
        table_type = TableType.objects.get(pk=pk)
    except TableType.DoesNotExist:
        return Response('table type not found', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TableTypeSerializer(table_type)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = TableTypeSerializer(table_type, data=request.DATA, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@restaurant_required
def list_or_create_table(request):
    if request.method == 'GET':
        serializer = TableSerializer(request.current_restaurant.tables.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.DATA.copy()
        serializer = TableSerializer(data=data)
        if serializer.is_valid():
            table = serializer.save()
            table.restaurant = request.current_restaurant
            table.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@restaurant_required
def get_or_update_table(request, pk):
    try:
        table = Table.objects.get(pk=pk)
    except Table.DoesNotExist:
        return Response('table not found', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TableSerializer(table)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = TableSerializer(table, data=request.DATA, partial=True)
        if serializer.is_valid():
            table = serializer.save()
            # 通过状态更改来判断是否叫号
            if request.DATA['status'] == 'waiting':
                # 对老的registration的处理
                try:
                    old_registration = table.registration
                    old_registration.table = None
                    old_registration.expire = True
                    old_registration.save()
                except:
                    pass

                registration = get_next_registration(table.table_type)
                if not registration:
                    serializer.data['registration'] = None
                    table.status = 'idle'
                    table.save()
                else:
                    serializer.data['registration'] = registration.id
                    registration.table = table
                    registration.save()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@restaurant_required
def table_type_registration(request):
    table_types = request.current_restaurant.table_types.all()
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
