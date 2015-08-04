#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from table.models import TableType, Table
from table.serializers import TableTypeSerializer
from table.serializers import TableTypeDetailSerializer
from table.serializers import TableSerializer
from table.serializers import TableDetailSerializer
from table.serializers import TableCreateSerializer

from restaurant.utils import restaurant_required


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


@api_view(['GET'])
@restaurant_required
def list_table_type_details(request):
    serializer = TableTypeDetailSerializer(request.current_restaurant.table_types.order_by('id'), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def list_table(request):
    """
    获取餐桌列表
    其中餐桌包含的订单状态有如下几种(0: 已下单，1: 待付款，2：已付款，3：已取消)
    ---
    serializer: table.serializers.TableSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
          message: table list
        - code: 400
          message: Bad Request
        - code: 401
          message: Not authenticated
    """
    tables = request.current_restaurant.tables.all()
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def create_table(request):
    """
    创建餐桌
    ---
    serializer: table.serializers.TableCreateSerializer
    omit_serializer: false

    responseMessages:
        - code: 201
          message: Created
        - code: 400
          message: Bad Request
        - code: 401
          message: Not authenticated
    """
    data = request.DATA.copy()
    serializer = TableCreateSerializer(data=data)
    if serializer.is_valid():
        match = re.search("\[(\d+)\-(\d+)\]", data['name'])
        if match:
            start_number, end_number = match.groups()
            split_list = re.split("\[\d+\-\d+\]", data['name'])
            ret = []
            for table_number in range(int(start_number), int(end_number)+1):
                table_data = request.DATA.copy()
                table_data['name'] = ('%s' % table_number).join(split_list)

                r_serializer = TableSerializer(data=table_data)
                if r_serializer.is_valid():
                    table = r_serializer.save()
                    table.restaurant = request.current_restaurant
                    table.save()
                    ret.append(r_serializer.data)

            return Response(ret, status=status.HTTP_201_CREATED)
        else:
            table = serializer.save()
            table.restaurant = request.current_restaurant
            table.save()
            return Response([serializer.data], status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@restaurant_required
def get_table(request, pk):
    """
    获取指定餐桌
    ---
    serializer: table.serializers.TableSerializer
    omit_serializer: false

    responseMessages:
        - code: 200 
          message: OK
        - code: 404
          message: Not Found
        - code: 401
          message: Not authenticated
    """
    try:
        table = Table.objects.get(pk=pk)
    except Table.DoesNotExist:
        return Response('table not found', status=status.HTTP_404_NOT_FOUND)
    serializer = TableSerializer(table)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def update_table(request, pk):
    """
    修改指定餐桌
    ---
    serializer: table.serializers.TableSerializer
    omit_serializer: false

    responseMessages:
        - code: 202
          message: Accepted
        - code: 404
          message: Not Found
        - code: 400
          message: Bad Request
        - code: 401
          message: Not authenticated
    """
    try:
        table = Table.objects.get(pk=pk)
    except Table.DoesNotExist:
        return Response('table not found', status=status.HTTP_404_NOT_FOUND)
    serializer = TableSerializer(table, data=request.DATA, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@restaurant_required
def delete_table(request, pk):
    """
    删除指定餐桌
    ---
    serializer: table.serializers.TableSerializer
    omit_serializer: false

    responseMessages:
        - code: 200 
          message: OK
        - code: 404
          message: Not Found
        - code: 401
          message: Not authenticated
    """
    try:
        table = Table.objects.get(pk=pk)
    except Table.DoesNotExist:
        return Response('table not found', status=status.HTTP_404_NOT_FOUND)
    table.delete()
    return Response(None, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def get_table_detail(request, pk):
    """
    获取全部餐桌详情
    ---
    serializer: table.serializers.TableDetailSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
          message: OK
        - code: 401
          message: Not authenticated
    """
    try:
        table = Table.objects.get(pk=pk)
    except Table.DoesNotExist:
        return Response('table not found', status=status.HTTP_404_NOT_FOUND)
    serializer = TableDetailSerializer(table)
    return Response(serializer.data, status=status.HTTP_200_OK)
