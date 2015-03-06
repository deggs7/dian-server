#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

import datetime
from functools import wraps

import qiniu
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RestaurantSerializer, TableTypeSerializer, TableTypeDetailSerializer
from .models import TableType
from .models import Restaurant
from dian.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY
from dian.settings import QINIU_BUCKET_PUBLIC


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


@api_view(["GET"])
def uptoken_default_restaurant(request):
    restaurants = request.user.own_restaurants.all()
    if restaurants:
        default = restaurants[0]
        auth = qiniu.Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
        uptoken = auth.upload_token(bucket=QINIU_BUCKET_PUBLIC, key="restaurant-%d" % default.id)
        return Response({
            "uptoken": uptoken
        })

    return Response('no default restaurant', status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_restaurant(request):
    data = request.DATA.copy()
    data["owner"] = request.user.pk
    serializer = RestaurantSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_restaurant(request):
    data = request.DATA.copy()
    try:
        restaurant = Restaurant.objects.get(pk=data.get("restaurant_id"))
    except Restaurant.DoesNotExist:
        return Response('restaurant not found', status=status.HTTP_404_NOT_FOUND)
    serializer = RestaurantSerializer(restaurant, data=data, partial=True)
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


@api_view(['GET'])
@restaurant_required
def list_table_type_details(request):
    serializer = TableTypeDetailSerializer(request.current_restaurant.table_types.order_by('id'), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# for statistics report
@api_view(['POST'])
@restaurant_required
def get_daily_registration(request):
    from_days_ago = request.DATA.get('since_days', 14)
    regs = request.current_restaurant.registrations
    now_day = datetime.datetime.now().date()
    from_day = now_day - datetime.timedelta(days=from_days_ago)
    day = 0
    ret = []
    while day <= from_days_ago:
        reg_day = from_day + datetime.timedelta(days=day)
        reg_count = regs.filter(create_time__gte=reg_day,
                                create_time__lt=reg_day+datetime.timedelta(days=1)).count()
        ret.append({
            "date": "%d月%d日" % (reg_day.month, reg_day.day),
            "reg_count": reg_count
        })
        day += 1

    return Response(ret, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def get_avg_waiting_time(request):
    from_days_ago = request.DATA.get('since_days', 14)
    regs = request.current_restaurant.registrations
    now_day = datetime.datetime.now().date()
    from_day = now_day - datetime.timedelta(days=from_days_ago)
    day = 0
    ret = []
    while day <= from_days_ago:
        reg_day = from_day + datetime.timedelta(days=day)
        t_regs = regs.filter(create_time__gte=reg_day,
                             create_time__lte=reg_day+datetime.timedelta(days=1))

        t_expired_regs = t_regs.filter(status__exact='expired', end_time__isnull=False)
        t_passed_regs = t_regs.filter(status__exact='passed', end_time__isnull=False)

        avg_waitime_expired = sum([(reg.end_time - reg.create_time).seconds for reg in t_expired_regs]) / t_expired_regs.count() \
            if t_expired_regs.count() else 0
        avg_waitime_passed = sum([(reg.end_time - reg.create_time).seconds for reg in t_passed_regs]) / t_passed_regs.count() \
            if t_passed_regs.count() else 0

        ret.append({
            "date": "%d月%d日" % (reg_day.month, reg_day.day),
            "avg_expired_value": avg_waitime_expired,
            "avg_passed_value": avg_waitime_passed
        })
        day += 1

    return Response(ret, status=status.HTTP_200_OK)


@api_view(['POST'])
@restaurant_required
def get_daily_type_registration(request):
    from_days_ago = request.DATA.get('since_days', 14)
    regs = request.current_restaurant.registrations
    now_day = datetime.datetime.now().date()
    from_day = now_day - datetime.timedelta(days=from_days_ago)
    day = 0
    ret = []
    while day <= from_days_ago:
        reg_day = from_day + datetime.timedelta(days=day)
        t_regs = regs.filter(create_time__gte=reg_day,
                             create_time__lt=reg_day+datetime.timedelta(days=1))
        t_expired_count = t_regs.filter(status__exact='expired').count()
        t_passed_count = t_regs.filter(status__exact='passed').count()

        ret.append({
            "date": "%d月%d日" % (reg_day.month, reg_day.day),
            "reg_expired_count": t_expired_count,
            "reg_passed_count": t_passed_count
        })
        day += 1

    return Response(ret, status=status.HTTP_200_OK)


# for history report
@api_view(['GET'])
@restaurant_required
def get_today_registration(request):
    ret = request.current_restaurant.registrations\
        .filter(create_time__gte=datetime.date.today(),
                status__in=['expired', 'passed'])\
        .order_by('-queue_number')
    from registration.serializers import RegistrationHistorySerializer
    serializer = RegistrationHistorySerializer(ret, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




