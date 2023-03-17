from rest_framework import serializers

from .models import CustomUser, Goods, Order


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
    user = serializers.StringRelatedField(source = 'user.email', read_only=True)
    
    class Meta:
        model = Goods
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для созданных заказов."""
    status = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(source = 'user.email', read_only=True)
    goods = serializers.PrimaryKeyRelatedField(
        # source = 'goods.id',
        many=True,
        queryset = Goods.objects.all()
    )
    
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        
        goods = validated_data.pop('goods')
        order = Order.objects.create(**validated_data)

        # for item in goods:
        #     order.goods.add(item)
        return order
        
