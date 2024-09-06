from django.urls import path

from apps.verifications.views import BindView, VerifyView

urlpatterns = [
    path('bind/', BindView.as_view()),
    path('verify/', VerifyView.as_view()),
]