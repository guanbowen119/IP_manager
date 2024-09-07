from django.urls import path

from apps.users.views import LoginView

urlpatterns = [
    path('devices/<username>/login', LoginView.as_view())
]