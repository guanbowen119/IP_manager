import re

from django.contrib.auth import authenticate
from django_redis import get_redis_connection
from prompt_toolkit.validation import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mobile', 'password', 'username')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    mobile = serializers.CharField(min_length=11, max_length=11)
    username = serializers.CharField(min_length=11, max_length=11)
    password = serializers.CharField(min_length=11, max_length=11, write_only=True)
    sms_code = serializers.CharField(min_length=4, max_length=4, write_only=True)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        sms_code = attrs.get('sms_code')

        redis_cli = get_redis_connection('code')
        redis_sms_code = redis_cli.get(mobile)
        # if redis_sms_code is None:
        #     raise ValidationError(message='短信验证码过期')
        # elif sms_code != redis_sms_code.decode():
        #     raise ValidationError(message='短信验证码错误')

        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))

        # 未注册就先注册
        if user is None:
            serializer = UserModelSerializer(data=attrs)
            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            else:
                serializer.save()
                attrs = serializer.data

        # 获得token
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        return data
