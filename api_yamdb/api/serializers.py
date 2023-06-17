import datetime
from rest_framework import serializers
import re
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import *


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


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset = Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset = Genre.objects.all(),
        slug_field='slug', many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'category', 'genre')
        model = Title

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        genre_data = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        title.category = category_data
        title.genre.set(genre_data)
        title.save()
        return title