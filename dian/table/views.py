#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from table.models import TableType, Table
from table.serializers import TableTypeSerializer
from table.serializers import TableTypeDetailSerializer
from table.serializers import TableSerializer
from table.serializers import TableDetailSerializer

from dian.utils import restaurant_required


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


@api_view(['POST', 'GET'])
@restaurant_required
def list_or_create_table(request):
    """
    创建餐桌 & 获取餐桌列表
    ---
        serializer: table.serializers.TableSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 201
              message: Created
            - code: 400
              message: Bad Request
            - code: 401
              message: Not authenticated
    """
    if request.method == 'GET':
        tables = []
        for table_type in request.current_restaurant.table_types.order_by('id'):
            tables.extend(table_type.tables.all())

        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.DATA.copy()
        serializer = TableSerializer(data=data)
        if serializer.is_valid():
            table = serializer.save()
            table.restaurant = request.current_restaurant
            table.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@restaurant_required
def get_or_update_or_delete_table(request, pk):
    """
    获取指定餐桌 & 修改指定餐桌 & 删除指定餐桌
    ---
        serializer: table.serializers.TableSerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 202
              message: Accepted
            - code: 404
              message: Not Found
            - code: 401
              message: Not authenticated
    """
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        table.delete()
        return Response(None, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def list_table_detail(request):
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
    tables = []
    for table_type in request.current_restaurant.table_types.order_by('id'):
        tables.extend(table_type.tables.all())

    serializer = TableDetailSerializer(tables, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
