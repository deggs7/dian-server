#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from trade.models import Cart
from trade.models import CartItem
from trade.models import Order
from trade.models import OrderItem
from menu.models import Product
from account.models import Member
from restaurant.models import Restaurant

from trade.serializers import CartSerializer
from trade.serializers import CartItemSerializer
from trade.serializers import OrderSerializer
from trade.serializers import OrderDetailSerializer


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def get_cart_by_restaurant(request):
    """
    获取购物车
    每个顾客访问每个餐厅，都会有一个对应的cart实体
    如果还没有对应的实例，则创建一个再返回
    param参数：openid —— restaurant的openid
              wp_openid —— member的openid
    ---
        serializer: trade.serializers.CartSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
    """
    openid = request.GET.get('openid')
    wp_openid = request.GET.get('wp_openid', None)
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('param error: no restaurant found', status=status.HTTP_400_BAD_REQUEST)
    try:
        member = Member.objects.get(wp_openid=wp_openid)
    except Member.DoesNotExist:
        return Response('param error: no member found', status=status.HTTP_400_BAD_REQUEST)

    cart = Cart.objects.get_or_create(restaurant=restaurant, member=member)[0]
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def add_cart_item(request):
    """
    添加一个商品至购物车，如果商品已经存在，则数量加1
    param参数：openid —— restaurant的openid
              wp_openid —— member的openid
    ---
        serializer: trade.serializers.CartItemSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
    """
    openid = request.GET.get('openid')
    wp_openid = request.GET.get('wp_openid', None)
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('param error: no restaurant found', status=status.HTTP_400_BAD_REQUEST)
    try:
        member = Member.objects.get(wp_openid=wp_openid)
    except Member.DoesNotExist:
        return Response('param error: no member found', status=status.HTTP_400_BAD_REQUEST)
    try:
        cart = Cart.objects.get(restaurant=restaurant, member=member)
    except Cart.DoesNotExist:
        return Response('param error: no cart found', status=status.HTTP_400_BAD_REQUEST)

    data = request.DATA.copy()
    cart_item = cart.cart_items.filter(product=int(data.get('product', None))).first()
    if cart_item:
        cart_item.count += 1
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def remove_cart_item(request):
    """
    在购物车中删除一个商品
    param参数：openid —— restaurant的openid
              wp_openid —— member的openid
    POST BODY:
              cart_id
              cart_item_id
    ---
        serializer: trade.serializers.CartSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
    """
    openid = request.GET.get('openid')
    wp_openid = request.GET.get('wp_openid', None)
    cart_id = request.DATA.get('cart_id', None)
    cart_item_id = request.DATA.get('cart_item_id', None)
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('param error: no restaurant found', status=status.HTTP_400_BAD_REQUEST)
    try:
        member = Member.objects.get(wp_openid=wp_openid)
    except Member.DoesNotExist:
        return Response('param error: no member found', status=status.HTTP_400_BAD_REQUEST)
    try:
        cart = Cart.objects.get(restaurant=restaurant, member=member)
        if cart.id != cart_id:
            return Response('param error: no volid cart', status=status.HTTP_400_BAD_REQUEST)
    except Cart.DoesNotExist:
        return Response('param error: no cart found', status=status.HTTP_400_BAD_REQUEST)
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id)
        if cart_item.cart != cart:
            return Response('param error: no valid cart item', status=status.HTTP_400_BAD_REQUEST)
    except CartItem.DoesNotExist:
        return Response('param error: no cart found', status=status.HTTP_400_BAD_REQUEST)

    cart_item.delete()
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def decrease_cart_item(request, pk):
    """
    减少购物车中商品数量或者删除购物车中该商品
    ---
        serializer: trade.serializers.CartItemSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
    """
    data = request.DATA.copy()
    try:
        cart_item = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        return Response('cart item not found', status=status.HTTP_404_NOT_FOUND)

    cart = cart_item.cart
    if cart_item.count > 1:
        cart_item.count -= 1
        cart_item.save()
    else:
        cart_item.delete()
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def update_cart(request, cart_pk):
    """
    更新购物车
    ---
        serializer: trade.serializers.CartSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
            - code: 404
              message: Not Found
    """
    try:
        cart = Cart.objects.get(pk=cart_pk)
    except CartItem.DoesNotExist:
        return Response('cart not found', status=status.HTTP_404_NOT_FOUND)

    cart_items = cart.cart_items.all()
    for cart_item in cart_items:
        cart_item.delete()

    for item in request.DATA:
        if 'productid' not in item or 'count' not in item:
            return Response('args error', status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(pk=item['productid'])
        except Product.DoesNotExist:
            return Response('product %d not found' % item['productid'], status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem(product=product, count=item['count'], cart=cart)
        cart_item.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def create_order_from_cart(request, cart_pk):
    """
    从购物车中创建订单
    param参数：openid —— restaurant的openid
              wp_openid —— member的openid
    ---
        serializer: trade.serializers.OrderDetailSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
    """
    openid = request.GET.get('openid')
    wp_openid = request.GET.get('wp_openid', None)

    try:
        cart = Cart.objects.get(pk=cart_pk)
    except Cart.DoesNotExist:
        return Response('cart not found', status=status.HTTP_400_BAD_REQUEST)
    try:
        restaurant = Restaurant.objects.get(openid=openid)
    except Restaurant.DoesNotExist:
        return Response('param error: no restaurant found', status=status.HTTP_400_BAD_REQUEST)
    try:
        member = Member.objects.get(wp_openid=wp_openid)
    except Member.DoesNotExist:
        return Response('param error: no member found', status=status.HTTP_400_BAD_REQUEST)

    order = Order(restaurant=restaurant, member=member)
    order.save()
    price_total = 0
    for cart_item in cart.cart_items.all():
        order_item = OrderItem(order=order,
                               category=cart_item.product.category.name,
                               name=cart_item.product.name,
                               img_key=cart_item.product.img_key,
                               price=cart_item.product.price,
                               unit=cart_item.product.unit,
                               description=cart_item.product.description,
                               count=cart_item.count
                               )
        order_item.save()
        price_total += cart_item.product.price * cart_item.count
        cart_item.delete()
    order.price = price_total
    order.save()

    serializer = OrderDetailSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def cancel_order(request, order_pk):
    """
    删除订单
    ---
        serializer: trade.serializers.OrderSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
    """
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response('order not found', status=status.HTTP_404_NOT_FOUND)

    for item in order.order_items.all():
        item.delete()
    order.delete()
    return Response(None, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def list_order(request):
    """
    获取历史订单列表
    param参数：
              wp_openid —— member的openid
    ---
        serializer: trade.serializers.OrderSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
    """
    wp_openid = request.GET.get('wp_openid', None)
    try:
        member = Member.objects.get(wp_openid=wp_openid)
    except Member.DoesNotExist:
        return Response('param error: no member found', status=status.HTTP_400_BAD_REQUEST)

    serializer = OrderSerializer(member.orders.exclude(status__in=[0, 1]), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def list_order_now(request):
    """
    获取当前订单列表 （待确认和已经确认）
    param参数：
              wp_openid —— member的openid
    ---
        serializer: trade.serializers.OrderSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
    """
    wp_openid = request.GET.get('wp_openid', None)
    try:
        member = Member.objects.get(wp_openid=wp_openid)
    except Member.DoesNotExist:
        return Response('param error: no member found', status=status.HTTP_400_BAD_REQUEST)

    serializer = OrderSerializer(member.orders.filter(status__in=[0, 1]), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes(())
@permission_classes(())
def get_detail_order(request, order_pk):
    """
    获取订单详细信息
    ---
        serializer: trade.serializers.OrderDetailSerializer
        omit_serializer: false

        responseMessages:
            - code: 200
              message: OK
            - code: 400
              message: Bad Request
            - code: 404
              message: Not Found
    """
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return Response('param error: no order found', status=status.HTTP_404_NOT_FOUND)

    serializer = OrderDetailSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


