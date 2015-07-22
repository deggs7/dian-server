# -*- encoding:utf-8 -*-
import random

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from account.models import Member

from photo.models import Tag
from photo.models import Photo

from photo.serializers import TagSerializer
from photo.serializers import PhotoSerializer

from photo.models import TAG_TYPE_ACTIVITY

@api_view(['GET'])
def get_next_photo_list(request):
    """
    获取下一个随机 n 个 photo, n 默认为 5
    ---

    responseMessages:
        - code: 400
          message: prama error
    """
    limit = request.GET.get('limit', 5)
    query_set = Photo.objects.all()
    random_query_set = set([])
    length = len(query_set)
    while (len(random_query_set) < int(limit)):
        rand_int = random.randint(0, length - 1)
        random_query_set.add(query_set[rand_int])
    serializer = PhotoSerializer(random_query_set)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def like_photo(request, photo_id=None):
    """
    赞一个 photo
    ---

    responseMessages:
        - code: 400
          message: prama error
    """
    member = request.member
    photo = Photo.objects.get(pk=photo_id)
    photo.likes.add(member)
    serializer = PhotoSerializer(photo)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_tag_with_restaurant(request, restaurant_openid):
    """
    获取 tag 的列表（餐厅入口），包含这家餐厅的tag还有全部的活动tag
    ---

    responseMessages:
        - code: 400
          message: prama error
    """
    query_set = Tag.objects.filter(restaurant__openid=restaurant_openid or\
            type=TAG_TYPE_ACTIVITY)
    serializer = TagSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_tag_with_activity(request):
    """
    获取 tag 的列表（活动入口），只列出全部的获得tag
    ---

    responseMessages:
        - code: 400
          message: prama error
    """
    query_set = Tag.objects.filter(type=TAG_TYPE_ACTIVITY)
    serializer = TagSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_photo(request):
    """
    获得我（当前 member）发过的 photo 的全部列表，并且每一项都是详细信息
    ---
    responseMessages:
        - code: 400
          message: prama error
    """
    pass


@api_view(['GET'])
def get_overview_of_my_photo(request):
    """
    获得我（当前 member）发过的 photo 的数量
    ---

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    member = request.member
    query_set = Photo.objects.filter(member=member)
    return Response({'count': len(query_set)},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def list_my_photo(request):
    """
    获得我（当前 member）发过的 photo 的全部列表，并且每一项都是详细信息
    ---
    responseMessages:
        - code: 400
          message: prama error
    """

    member = request.member
    query_set = Photo.objects.filter(member=member)
    serializer = PhotoSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_overview_of_my_like(request):
    """
    获得我（当前 member）赞过的 photo 的数量
    ---

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    member = request.member
    query_set = member.like_photos.all()
    return Response({'count': len(query_set)},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def list_my_like(request):
    """
    获得我（当前 member）赞过的 photo 的全部列表，并且每一项都是详细信息
    ---
    serializer: photo.serializers.PhotoSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    member = request.member
    query_set = member.like_photos.all()
    serializer = PhotoSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


