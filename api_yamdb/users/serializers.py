from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import User
from .validators import validate_username


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254
    )
    username = serializers.CharField(
        max_length=150,
        validators=(validate_username,)
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if username == 'me':
            raise ValidationError('Использование "me" в качестве '
                                  'username запрещено')
        if not User.objects.filter(username=username,
                                   email=email).exists():
            if User.objects.filter(username=data.get('username')):
                raise serializers.ValidationError(
                    'Пользователь с таким username уже существует'
                )
            if User.objects.filter(email=data.get('email')):
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует'
                )
        return data

    class Meta:
        model = User
        fields = ['email', 'username']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = (
            'username',
            'confirmation_code',
        )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]


class UsersMeSerializer(UsersSerializer):
    class Meta:
        model = User
        fields = UsersSerializer.Meta.fields
        read_only_fields = ['role']
