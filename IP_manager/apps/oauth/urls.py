from django.urls import path

from apps.oauth.views import LarkRedirectAPIView, LarkBindGenericAPIView

urlpatterns = [
    path('lark_redirect/', LarkRedirectAPIView.as_view()),
    path('lark_bind/', LarkBindGenericAPIView.as_view()),
]