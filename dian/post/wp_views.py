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
    if not member_id:
        member_id = request.member
    query_set = Post.objects.filter(member=member_id)
    serializer = PostSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_overview_of_my_post(request, member_id=None):
    if not member_id:
        member_id = request.member
    query_set = Post.objects.filter(member=member_id)
    return Response({'count': len(query_set)},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def list_my_like(request, member_id=None):
    if not member_id:
        member_id = request.member
    query_set = Like.objects.filter(member=member_id)
    serializer = LikeSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_overview_of_my_like(request, member_id=None):
    if not member_id:
        member_id = request.member
    query_set = Like.objects.filter(member=member_id)
    return Response({'count': len(query_set)},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def like_post(request, post_id=None, member_id=None):
    if not member_id:
        member_id = request.member

    post = Post.objects.get(id=post_id)
    member = Member.objects.get(id=member_id)
    like = Like.objects.create(member=member, post=post)
    like.save()
    serializer = LikeSerializer(like)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_tag_with_restaurant(request, restaurant_openid):
    query_set = Tag.objects.filter(restaurant__openid=restaurant_openid)
    serializer = TagSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_tag_with_activity(request):
    query_set = Tag.objects.filter(type=0)
    serializer = TagSerializer(query_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
