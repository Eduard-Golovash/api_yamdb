from rest_framework import serializers
import re
from rest_framework.exceptions import ValidationError

from reviews.models import *


class UsersSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        RegisterUserSerializer(self, value)
        return value

    def validate_email(self, value):
        RegisterUserSerializer(self, value)
        return value

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


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Использование "me" в качестве '
                                  'username запрещено')
        reg = re.compile(r'^[\w.@+-]+\Z')
        if re.match(reg, value) is None:
            raise ValidationError('Только буквы, цифры и @/./+/-/_.')
        if User.objects.filter(username=value).first():
            raise ValidationError('Username уже занят')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).first():
            raise ValidationError('Email уже занят')
        return value

    class Meta:
        fields = ['email', 'username']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = (
            'username',
            'confirmation_code',
        )
