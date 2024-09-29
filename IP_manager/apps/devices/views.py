import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.devices.serializers import DeviceModelSerializer
from apps.devices.utils import generate_token, check_token
from utils.Authentication import CsrfExemptSessionAuthentication
from utils.get_client_ip import get_client_ip


class BindAPIView(APIView):
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


class VerifyGenericAPIView(GenericAPIView):
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


class DeviceListGenericAPIView(GenericAPIView):
    serializer_class = DeviceModelSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        data = self.get_serializer(request.user.devices, many=True).data
        return Response(data={'status': 'success', 'devices': data}, status=status.HTTP_200_OK)


class DeviceDeleteGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @staticmethod
    def delete(request, device_id):
        try:
            device = request.user.devices.get(id=device_id)
        except ObjectDoesNotExist:
            return Response({'status': 'error', 'message': 'Device not found'}, status=status.HTTP_400_BAD_REQUEST)
        device.delete()
        return Response(data={'status': "success", "message": "Device unbound successfully"}, status=status.HTTP_204_NO_CONTENT)


class DeviceLoginAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @staticmethod
    def post(request, device_id):
        try:
            device = request.user.devices.get(id=device_id)
        except ObjectDoesNotExist:
            return Response({'status': 'error', 'message': 'Device not found'}, status=status.HTTP_400_BAD_REQUEST)

        url = 'https://yxms.byr.ink/api/login'
        response = requests.post(url, json={'username': request.user.username, 'ip': device.ip})

        if response.status_code == 200 and response.json()['success'] == True:
            device.logged_in = True
            return Response(data={'status': 'success', 'message': 'Device logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'status': 'deny', 'message': 'Login denied'}, status=status.HTTP_403_FORBIDDEN)



class DeviceLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @staticmethod
    def get(request, device_id):
        try:
            device = request.user.devices.get(id=device_id)
        except ObjectDoesNotExist:
            return Response({'status': 'error', 'message': 'Device not found'}, status=status.HTTP_400_BAD_REQUEST)
        device.logged_in = False
        device.save()
        return Response(data={'status': 'success', 'message': 'Device logged out successfully'}, status=status.HTTP_200_OK)