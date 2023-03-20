from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GoodsViewSet, OrderViewSet #UserViewSet

router = DefaultRouter()

# router.register('users', UserViewSet)
router.register('goods', GoodsViewSet, basename='goods')
router.register('orders', OrderViewSet, basename='orders')


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
