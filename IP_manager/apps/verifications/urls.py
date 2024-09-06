from django.urls import path

from apps.verifications.views import BindView

urlpatterns = [
    path('bind/', BindView.as_view())
]