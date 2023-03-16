from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

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
