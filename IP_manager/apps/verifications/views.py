from django.http import JsonResponse
from django.views import View

from apps.verifications.utils import generate_token
from utils.get_client_ip import get_client_ip


class BindView(View):

    @staticmethod
    def post(request):
        client_ip = get_client_ip(request)
        token = generate_token(client_ip)
        return JsonResponse({
            "status": "success",
            "token": token
            })