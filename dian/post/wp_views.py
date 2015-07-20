# -*- encoding:utf-8 -*-
import random

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from account.models import Member

from post.models import Tag
from post.models import Image
from post.models import Post

from post.serializers import TagSerializer
from post.serializers import ImageSerializer
from post.serializers import PostSerializer


@api_view(['GET'])
def get_next_post_list(request, limit=5):
    """
    获取下一个随机 n 个 post, n 默认为 5
    ---
    serializer: post.serializers.PostSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    query_set = Post.objects.all()
    random_query_set = set([])
    length = len(query_set)
    while (len(random_query_set) < int(limit)):
        rand_int = random.randint(0, length - 1)
        random_query_set.add(query_set[rand_int])
    serializer = PostSerializer(random_query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_my_post(request, member_id=None):
    """
    获得我（当前 member）发过的 post 的全部列表，并且每一项都是详细信息
    ---
    serializer: post.serializers.PostSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """

    if not member_id:
        member_id = request.member
    query_set = Post.objects.filter(member=member_id)
    serializer = PostSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_overview_of_my_post(request, member_id=None):
    """
    获得我（当前 member）发过的 post 的数量
    ---
    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    if not member_id:
        member_id = request.member
    query_set = Post.objects.filter(member=member_id)
    return Response({'count': len(query_set)},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def list_my_like(request, member_id=None):
    """
    获得我（当前 member）赞过的 post 的全部列表，并且每一项都是详细信息
    ---
    serializer: post.serializers.PostSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    if not member_id:
        member_id = request.member
    member_obj = Member.objects.get(id=member_id)
    query_set = member_obj.like_posts.all()
    serializer = PostSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_overview_of_my_like(request, member_id=None):
    """
    获得我（当前 member）赞过的 post 的数量
    ---
    serializer: menu.serializers.MenuDetailSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    if not member_id:
        member_id = request.member
    member_obj = Member.objects.get(id=member_id)
    query_set = member_obj.like_posts.all()
    return Response({'count': len(query_set)},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def like_post(request, post_id=None, member_id=None):
    """
    赞一个 post
    ---
    serializer: post.serializers.PostSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    if not member_id:
        member_id = request.member

    post_obj = Post.objects.get(id=post_id)
    member_obj = Member.objects.get(id=member_id)
    post_obj.likes.add(member_obj)
    serializer = PostSerializer(post_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_tag_with_restaurant(request, restaurant_openid):
    """
    获取 tag 的列表（餐厅入口）
    ---
    serializer: post.serializers.TagSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    query_set = Tag.objects.filter(restaurant__openid=restaurant_openid)
    serializer = TagSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_tag_with_activity(request):
    """
    获取 tag 的列表（活动入口）
    ---
    serializer: post.serializers.TagSerializer
    omit_serializer: false

    responseMessages:
        - code: 200
        - code: 400
          message: prama error
    """
    query_set = Tag.objects.filter(type=0)
    serializer = TagSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
