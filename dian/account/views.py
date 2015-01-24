from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer


@api_view(["GET"])
def get_my_account(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["PUT"])
def change_passwd(request):
    data = request.DATA.copy()
    new_password1 = data.get('new_password1', None)
    new_password2 = data.get('new_password2', None)

    if not new_password1 or new_password1 != new_password2:
        return Response({"error": "password input error"},
                        status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(new_password1)
    request.user.save()

    return Response({"info": "change password done"}, status=status.HTTP_202_ACCEPTED)




