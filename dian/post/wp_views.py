#! -*- encoding:utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from post.models import Tag
from post.models import Like
from post.models import Image
from post.models import Post


@api_view(['GET'])
def list_post(request):
    return Response("Hello list_post", status=status.HTTP_200_OK)


@api_view(['POST'])
def create_post():
    pass


@api_view(['GET'])
def get_post():
    pass


@api_view(['POST'])
def update_post():
    pass


@api_view(['GET'])
def list_tag(request):
    data = Tag.objects.all()
    return Response(str(data), status=status.HTTP_200_OK)


@api_view(['POST'])
def create_tag():
    pass


@api_view(['GET'])
def get_tag():
    pass


@api_view(['TAG'])
def update_tag():
    pass
