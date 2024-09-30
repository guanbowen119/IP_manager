from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.users.serializers import UserModelSerializer
from utils.Authentication import CsrfExemptSessionAuthentication


class LoginView(APIView):
    serializer_class = UserModelSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @staticmethod
    def post(request):
        data = request.data.dict()
        mobile = data.get('mobile')
        sms_code = data.get('sms_code')

        if not all([mobile, sms_code]):
            return Response({'errmsg': '参数不全'}, status=status.HTTP_400_BAD_REQUEST)

        redis_cli = get_redis_connection('code')
        redis_image_code = redis_cli.get(mobile)
        if redis_image_code is None:
            return Response({'errmsg': '短信验证码过期'}, status=status.HTTP_400_BAD_REQUEST)
        elif sms_code != redis_image_code.decode():
            return Response({'errmsg': '短信验证码错误'}, status=status.HTTP_400_BAD_REQUEST)

        User.USERNAME_FIELD = 'mobile'
        user = authenticate(username=mobile, password=mobile)

        if user is None:
            data['password'] = mobile
            data['username'] = mobile
            serializer = UserModelSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                user = serializer.instance

        login(request, user)
        request.session.set_expiry(None)
        response = Response(status=status.HTTP_200_OK)
        return response



class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        data['password'] = data['mobile']
        data['username'] = data['mobile']
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @staticmethod
    def get(request):
        logout(request)
        return Response({'msg': '登出成功'}, status=status.HTTP_200_OK)
