import logging
from rest_framework import status
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from market.permissions import AuthorOrStaffPermission

from .models import CustomUser, Goods, Order
from .serializers import (
    GetOrderSerializer,
    GoodsSerializer,
    OrderSerializer,
    UserSerializer,
    UpdateOrderSerializer,
)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
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
        logging.info('goodsasa')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class OrderViewSet(ModelViewSet):

    permission_classes = (AuthorOrStaffPermission,)
    http_method_names = ['get', 'post', 'head', 'put']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-id')
        return Order.objects.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetOrderSerializer
        if self.request.method == 'PUT':
            return UpdateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        logging.info(f'serializer {serializer}')
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        serializer.save(processed_by=self.request.user)


class APIOrders(APIView):

    def get(self, request):
        user = self.request.user
        all_orders = Order.objects.all().order_by('-pub_date')
        if user.is_staff:
            serializer = GetOrderSerializer(all_orders, many=True)
            return Response(serializer.data)
        user_orders = Order.objects.filter(user=user).order_by('-pub_date')
        serializer = GetOrderSerializer(user_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = self.request.user
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
