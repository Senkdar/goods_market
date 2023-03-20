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
    user = serializers.StringRelatedField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = Goods
        fields = '__all__'


class GetOrderSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра заказов."""
    goods = GoodsSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(
        source='user.email',
        read_only=True
    )
    processed_by = serializers.StringRelatedField(
        source='user.username',
        read_only=True
    )
    pub_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    processed_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'pub_date', 'goods',
            'status', 'processed_by', 'processed_at', 'comment')

    def to_representation(self, instance):
        order = super().to_representation(instance)
        status = order['status']
        if status == 'created':
            order.pop('processed_at')
            order.pop('processed_by')
            order.pop('comment')
        if status == 'approved':
            order.pop('comment')
        return order


class GoodsPKfield(serializers.PrimaryKeyRelatedField):
    """Переопределяем queryset для товаров в заказе, чтобы
    пользователь мог выбрать только те товары, которые он добавил.
    """
    def get_queryset(self):
        user = self.context.get('request').user
        queryset = Goods.objects.filter(user=user)
        return queryset

    def to_internal_value(self, data):
        """При попытке добавить id товаров, не принадлежащих
        пользователю, будет сообщение об ошибке.
        """
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError:
            raise serializers.ValidationError(f'У Вас нет товара с id {data}')


class CreateOrderSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказов пользователем."""
    status = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(source='user.email', read_only=True)
    goods = GoodsPKfield(many=True)

    class Meta:
        model = Order
        fields = ('id', 'goods', 'user', 'status', 'pub_date')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return GetOrderSerializer(instance, context=context).data

    def create(self, validated_data):
        goods = validated_data.pop('goods')
        order = Order.objects.create(**validated_data)
        for item in goods:
            order.goods.add(item)
        return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления заказа администратором."""
    ORDER_STATUSES = (
        ('created', 'Создан'),
        ('rejected', 'Отклонен'),
        ('approved', 'Одобрен'),
    )
    processed_by = serializers.StringRelatedField(
        source='user.username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    status = serializers.ChoiceField(choices=ORDER_STATUSES)
    processed_at = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M:%S',
        read_only=True
    )

    class Meta:
        model = Order
        fields = ('status', 'processed_by', 'processed_at', 'comment')
