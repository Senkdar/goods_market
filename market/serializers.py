from rest_framework import serializers
import logging
from .models import CustomUser, Goods, Order

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'last_name',
            'first_name',
            'patronymic',
            'email',
            'password',
            'phone_number',
        )

    def create(self, validated_data):
        """Создание нового пользователя."""
        user = CustomUser.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data['patronymic'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class GoodsSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров."""
    user = serializers.StringRelatedField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = Goods
        fields = '__all__'


class GetOrderSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра созданных заказов."""
    goods = GoodsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для созданных заказов."""
    status = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(source='user.email', read_only=True)
    goods = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Goods.objects.all()
    )

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):

        goods = validated_data.pop('goods')
        order = Order.objects.create(**validated_data)
        for item in goods:
            order.goods.add(item)
        return order

    def validate(self, data):
        goods_data = data['goods']
        user = self.context.get('request').user
        goods = Goods.objects.filter(user=user)
        for item in goods_data:
            if item not in goods:
                raise serializers.ValidationError(
                    {'status': f'У Вас нет товара с id {item.id}'}
                )
        return data
