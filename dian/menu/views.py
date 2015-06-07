#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dian.utils import restaurant_required

from menu.models import Menu
from menu.models import Category
from menu.models import Product

from menu.serializers import MenuSerializer
from menu.serializers import CategorySerializer
from menu.serializers import ProductSerializer


@api_view(['POST'])
@restaurant_required
def create_menu(request):
    """
    创建菜单
    ---
        serializer: menu.serializers.MenuSerializer
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
    serializer = MenuSerializer(data=data)
    if serializer.is_valid():
        menu = serializer.save()
        menu.restaurant = request.current_restaurant
        menu.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@restaurant_required
def list_menu(request):
    """
    菜单列表
    ---
        serializer: menu.serializers.MenuSerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    serializer = MenuSerializer(request.current_restaurant.menus.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def get_menu(request, pk):
    """
    获取指定菜单
    ---
        serializer: menu.serializers.MenuSerializer
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
        menu = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response('menu type not found', status=status.HTTP_404_NOT_FOUND)

    serializer = MenuSerializer(menu)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@restaurant_required
def update_menu(request, pk):
    """
    修改指定菜单
    ---
        serializer: menu.serializers.MenuSerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 400
              message: Bad Request
            - code: 404
              message: Not Found
            - code: 401
              message: Not authenticated
    """
    try:
        menu = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response('menu type not found', status=status.HTTP_404_NOT_FOUND)

    serializer = MenuSerializer(menu, data=request.DATA, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@restaurant_required
def delete_menu(request, pk):
    """
    删除指定菜单
    ---
        serializer: menu.serializers.MenuSerializer
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
        menu = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response('menu type not found', status=status.HTTP_404_NOT_FOUND)

    menu.delete()
    return Response(None, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def create_category(request):
    """
    创建分类
    ---
        serializer: menu.serializers.CategorySerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def get_category(request, pk):
    """
    获取指定分类
    ---
        serializer: menu.serializers.CategorySerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['PUT'])
@restaurant_required
def update_category(request, pk):
    """
    修改指定分类
    ---
        serializer: menu.serializers.CategorySerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@restaurant_required
def delete_category(request, pk):
    """
    删除指定分类
    ---
        serializer: menu.serializers.CategorySerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def list_category_by_menu(request, pk):
    """
    分类列表
    ---
        serializer: menu.serializers.CategorySerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def create_product(request):
    """
    创建商品
    ---
        serializer: menu.serializers.ProductSerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def get_product(request, pk):
    """
    获取指定商品
    ---
        serializer: menu.serializers.ProductSerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['PUT'])
@restaurant_required
def update_product(request, pk):
    """
    修改指定商品
    ---
        serializer: menu.serializers.ProductSerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@restaurant_required
def delete_product(request, pk):
    """
    删除指定商品
    ---
        serializer: menu.serializers.ProductSerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


@api_view(['GET'])
@restaurant_required
def list_product_by_category(request, pk):
    """
    商品列表
    ---
        serializer: menu.serializers.ProductSerializer
        omit_serializer: false

        responseMessages:
            - code: 200 
              message: OK
            - code: 401
              message: Not authenticated
    """
    return Response(None, status=status.HTTP_200_OK)


