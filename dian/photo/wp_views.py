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
    parameters:
        - name: limit
          type: integer
          paramType: query
          required: false

    serializer: PhotoSerializer

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
    serializer: PhotoSerializer

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
    serializer: TagSerializer

    responseMessages:
        - code: 400
          message: prama error
    """
    
    # TODO: 获取餐厅的tag，同时再获取全部的活动tag
    tag_restaurant = Tag.objects.filter(restaurant__openid=restaurant_openid)
    tag_activity = Tag.objects.filter(type=TAG_TYPE_ACTIVITY)
    serializer = TagSerializer(tag_restaurant, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_tag_with_activity(request):
    """
    获取 tag 的列表（活动入口），只列出全部的获得tag
    ---
    serializer: TagSerializer

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
    发布图片，并返回新创建的图片信息
    ---
    parameters:
        - name: file_key
          type: string
          paramType: form
          required: true
        - name: tag
          type: integer
          paramType: form
          required: true

    serializer: PhotoSerializer

    responseMessages:
        - code: 400
          message: prama error
    """
    pass


@api_view(['GET'])
def get_overview_of_my_photo(request):
    """
    获得我（当前 member）发过的 photo 数量的统计（见原型）
    ---
    type:
        total:
            required: true
            type: integer 
        reward:
            required: true
            type: integer
        like:
            required: true
            type: integer

    responseMessages:
        - code: 400
          message: prama error
    """
    member = request.member
    query_set = Photo.objects.filter(member=member)

    # TODO: 根据原型统计返回的信息
    rt = {
            'count': len(query_set),
        }

    return Response(rt, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_my_photo(request):
    """
    获得我（当前 member）发过的 photo 的全部列表，并且每一项都是详细信息
    ---
    serializer: PhotoSerializer

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
    type:
        total:
            required: true
            type: integer 

    responseMessages:
        - code: 400
          message: prama error
    """
    member = request.member
    query_set = member.like_photos.all()
    rt = {
            'total': len(query_set),
            }
    return Response(rt, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_my_like(request):
    """
    获得我（当前 member）赞过的 photo 的全部列表，
    并且每一项都是详细信息
    ---
    serializer: PhotoSerializer

    responseMessages:
        - code: 400
          message: prama error
    """
    member = request.member
    query_set = member.like_photos.all()
    serializer = PhotoSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


