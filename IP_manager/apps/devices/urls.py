from django.urls import path

from apps.devices.views import BindView, VerifyView, DeviceListAPIView

urlpatterns = [
    path('bind/', BindView.as_view()),
    path('verify/', VerifyView.as_view()),
    path('devices/', DeviceListAPIView.as_view()),
]