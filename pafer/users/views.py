from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import get_token_by_user
from .serializers import UserSignInSerializer, UserSignUpSerializer


class UserSignUpAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        user = serializer.instance
        datas = serializer.data
        token = get_token_by_user(user)
        datas['token'] = token

        headers = self.get_success_headers(serializer)
        return Response(data=datas, status=status.HTTP_201_CREATED, headers=headers)

class UserSignInAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED)