from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import obtain_jwt_token

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

def get_token_by_user(user):
    payload = JWT_PAYLOAD_HANDLER(user)
    token = JWT_ENCODE_HANDLER(payload)
    return token

class UserSignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)

    default_error_messages = {
        "diff_password": "Those passwords do not match."
    }

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')

    def validate(self, datas):
        username, email = datas.get('username'), datas.get('email')
        password, confirm_password = datas.get('password'), datas.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'message': self.error_messages.get('diff_password')})
        else:
            datas['password'] = make_password(password)
            return datas
        

class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    default_error_messages = {
        "fail_authenticate": "Failed to authenticate login."
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, datas):
        username, email, password = datas.get('username'), datas.get('email'), datas.pop('password')
        self.user = authenticate(username=username, password=password)

        if self.user:
            token = get_token_by_user(self.user)
            update_last_login(None, self.user)

            datas['token'] = token
            return datas
        else:
            raise serializers.ValidationError({'message': self.error_messages.get('fail_authenticate')})