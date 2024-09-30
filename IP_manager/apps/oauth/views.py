from django.contrib.auth import login
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.oauth.models import OAuthLarkUser
from apps.oauth.serializers import OAuthLarkUserModelSerializer
from apps.oauth.utils import get_user_access_token, get_user_info, generate_token, check_token
from apps.users.models import User
from utils.Authentication import CsrfExemptSessionAuthentication


# Create your views here.
class LarkRedirectAPIView(APIView):
    @staticmethod
    def get(request):
        code = request.query_params.get('code')
        user_access_token = get_user_access_token(code)
        user_info = get_user_info(user_access_token)

        try:
            oauth_user = OAuthLarkUser.objects.get(openid=user_info.get('openid'))
            login(request, oauth_user.user)
            return Response(data={'msg': '登陆成功'}, status=status.HTTP_200_OK)
        except OAuthLarkUser.DoesNotExist:
            open_id_token = generate_token(user_info.get('open_id'))
            return Response(data={'open_id_token': open_id_token, 'msg': '请绑定账号'}, status=status.HTTP_200_OK)


class LarkBindGenericAPIView(GenericAPIView):
    serializer_class = OAuthLarkUserModelSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        data = request.data
        mobile = data.get('mobile')
        sms_code = data.get('sms_code')
        open_id_token = data.get('open_id_token')

        # redis_cli = get_redis_connection('code')
        # redis_image_code = redis_cli.get(mobile)
        # if redis_image_code is None:
        #     return Response({'errmsg': '短信验证码过期'}, status=status.HTTP_400_BAD_REQUEST)
        # elif sms_code != redis_image_code.decode():
        #     return Response({'errmsg': '短信验证码错误'}, status=status.HTTP_400_BAD_REQUEST)

        open_id = check_token(open_id_token)
        user = User.objects.get(mobile=mobile)

        serializer = self.get_serializer(data={'openid': open_id, 'user': user.id})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()

        login(request, user)
        return Response(data={'msg': '绑定成功'}, status=status.HTTP_200_OK)