from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser, Goods, Order
from .serializers import (
    GoodsSerializer,
    OrderSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminUser,)


class GoodsViewSet(ModelViewSet):

    serializer_class = GoodsSerializer

    def get_queryset(self):
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

    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        user = self.request.user
        goods = Goods.objects.filter(user=user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, goods=goods)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        ) 
