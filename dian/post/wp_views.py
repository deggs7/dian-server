#! -*- encoding:utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


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
