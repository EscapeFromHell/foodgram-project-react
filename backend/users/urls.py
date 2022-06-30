from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import SubscribeViewSet, TokenView

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register(r'users', SubscribeViewSet, basename='users')

urlpatterns = [
    path('auth/token/login/', TokenView.as_view(), name="login"),
    path('auth/token/logout/', TokenDestroyView.as_view(), name="logout"),
    path('', include(router_v1.urls)),
]
