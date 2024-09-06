from django.http import JsonResponse
from django.views import View

from apps.devices.utils import generate_token
from utils.get_client_ip import get_client_ip
from utils.views import LoginRequiredJSONMixin


class BindView(LoginRequiredJSONMixin, View):
    """
    申请绑定邮箱和设备
    """
    @staticmethod
    def post(request):
        client_ip = get_client_ip(request)
        token = generate_token(client_ip)
        return JsonResponse({"status": "success", "token": token})


class VerifyView(LoginRequiredJSONMixin, View):
    """
    绑定邮箱和设备
    """
    @staticmethod
    def post(request):
        import json
        data = json.loads(request.body)
        token_ip = data.get('token')

        if not token_ip:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token'})

        client_ip = get_client_ip(request)

        if token_ip != client_ip:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token'})

        # TODO

        return JsonResponse({"status": "success", "message": "Device bound successfully"})