from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser, Goods, Order
from .serializers import (
    GetOrderSerializer,
    GoodsSerializer,
    CreateOrderSerializer,
    MyUserSerializer,
    UpdateOrderSerializer,
)
from .permissions import AuthorOrAdminPermission


# class UserViewSet(ModelViewSet):
#     """Вьюсет для пользователей."""
#     serializer_class = MyUserSerializer
#     queryset = CustomUser.objects.all()
#     permission_classes = (IsAdminUser,)


class GoodsViewSet(ModelViewSet):
    """Вьюсет для товаров."""
    serializer_class = GoodsSerializer
    permission_classes = (AuthorOrAdminPermission,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Goods.objects.all()
        return Goods.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class OrderViewSet(ModelViewSet):
    """Вьюсет для заказов."""
    permission_classes = (AuthorOrAdminPermission,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetOrderSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateOrderSerializer
        return CreateOrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-id')
        return Order.objects.filter(user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        serializer.save(processed_by=self.request.user)
        instance = serializer.instance
        instance.processed_at = timezone.now()
        instance.save()
