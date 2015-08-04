from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes 
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from .serializers import SeedUserSerializer


@api_view(["GET"])
def get_my_account(request):
    """
    获取当前登陆的账号信息
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["PUT"])
def change_passwd(request):
    """
    更改密码
    """
    data = request.DATA.copy()
    old_password = data.get('old_password', None)
    new_password1 = data.get('new_password1', None)
    new_password2 = data.get('new_password2', None)

    if not old_password or not request.user.check_password(old_password):
        return Response({}, status=status.HTTP_403_FORBIDDEN)

    if not new_password1 or new_password1 != new_password2:
        return Response({"error": "password input error"},
                        status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(new_password1)
    request.user.save()

    return Response({"info": "change password done"}, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
@authentication_classes(())
@permission_classes(())
def create_seed_user(request):
    """
    创建种子用户，为门户页面上提交开通申请而设置的
    """
    data = request.DATA.copy()
    serializer = SeedUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

