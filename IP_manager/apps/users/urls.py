from django.urls import path

from apps.users.views import MyTokenObtainPairView, LoginView, LogoutView

urlpatterns = [
    path('users/login/', LoginView.as_view()),  # 方案1使用Session登陆
    # path('users/login/', MyTokenObtainPairView.as_view(), name='login'),  # 方案2使用Token登陆，但登出较为麻烦
    path('users/logout/', LogoutView.as_view())
]