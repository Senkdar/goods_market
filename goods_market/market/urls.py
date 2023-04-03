from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GoodsViewSet, OrderViewSet

router = DefaultRouter()

router.register('goods', GoodsViewSet, basename='goods')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
