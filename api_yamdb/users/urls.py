from django.urls import include, path
from rest_framework import routers

from .views import (
    GetTokenAPIView,
    RegisterUserAPIView,
)


app_name = 'users'


router_v1 = routers.DefaultRouter()


auth_urls_v1 = [
    path('auth/signup/', RegisterUserAPIView.as_view(), name='signup'),
    path('auth/token/', GetTokenAPIView.as_view(), name='get_token'),
]

urlpatterns = [
    path('', include(auth_urls_v1)),
    path('', include(router_v1.urls)),
]
