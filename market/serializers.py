from rest_framework import serializers

from .models import CustomUser, Goods, Order


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    class Meta:
        model = CustomUser
        fields = (
            'last_name',
            'first_name',
            'patronymic',
            'email',
            'password',
            'phone_number',
        )


class GoodsSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров."""
    user = serializers.StringRelatedField(source = 'user.email', read_only=True)
    
    class Meta:
        model = Goods
        fields = '__all__'