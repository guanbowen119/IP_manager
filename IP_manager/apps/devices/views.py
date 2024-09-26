from types import GenericAlias

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet

from apps.devices.models import Device
from apps.devices.serializers import DeviceModelSerializer
from apps.devices.utils import generate_token, check_token
from utils.Authentication import CsrfExemptSessionAuthentication
from utils.get_client_ip import get_client_ip


class BindView(APIView):
    """
    申请绑定邮箱和设备
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @staticmethod
    def post(request):
        client_ip = get_client_ip(request)
        token = generate_token(client_ip)
        return Response({"status": "success", "token": token}, status=status.HTTP_200_OK)


class VerifyView(GenericAPIView):
    """
    绑定邮箱和设备
    """
    serializer_class = DeviceModelSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @staticmethod
    def post(request):
        data = request.data
        token_ip = check_token(data.get('token'))

        if not token_ip:
            return Response({'status': 'error', 'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        client_ip = get_client_ip(request)

        if token_ip != client_ip:
            return Response({'status': 'error', 'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceModelSerializer(data={'user': request.user.id, 'ip': token_ip})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            pass

        return Response({"status": "success", "message": "Device bound successfully"}, status=status.HTTP_200_OK)


class DeviceListDeleteAPIView(ListAPIView, DestroyAPIView):
    queryset = Device.objects.all()
