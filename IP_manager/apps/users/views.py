import json

from django.http import JsonResponse
from django.views import View


class LoginView(View):
    @staticmethod
    def post(request, username):
        data = json.loads(request.body)
        if not username:
            return JsonResponse({})