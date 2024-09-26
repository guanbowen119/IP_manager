from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LoginRequiredJSONMixin(LoginRequiredMixin):

    @staticmethod
    def handle_no_permission(**kwargs):
        return JsonResponse({'errmsg': '没有登陆'})
