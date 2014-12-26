from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


@api_view(["GET"])
def get_my_account(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
