from django.urls import path

from apps.devices.views import BindAPIView, VerifyGenericAPIView, DeviceListGenericAPIView, DeviceDeleteGenericAPIView, \
    DeviceLoginAPIView, DeviceLogoutAPIView

urlpatterns = [
    path('bind/', BindAPIView.as_view()),
    path('verify/', VerifyGenericAPIView.as_view()),
    path('devices/', DeviceListGenericAPIView.as_view()),
    path('devices/<device_id>/', DeviceDeleteGenericAPIView.as_view()),
    path('devices/<device_id>/login/', DeviceLoginAPIView.as_view()),
    path('devices/<device_id>/logout/', DeviceLogoutAPIView.as_view()),
]