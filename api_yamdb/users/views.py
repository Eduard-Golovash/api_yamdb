from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import permissions
from rest_framework import generics, status
from rest_framework.response import Response

from reviews.models import User
from api.send_util import send_confirmation_code
from .serializers import (
    RegisterUserSerializer,
    TokenSerializer,)

codegen = PasswordResetTokenGenerator()


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer  

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterUserSerializer(data=data)
        confirmation_code = Token.generate_key()
        user = User.objects.filter(**data).first()
        if user:
            user.confirmation_code = user.confirmation_code
            user.save()
        else:
            serializer.is_valid(raise_exception=True)
            User.objects.create(**serializer.validated_data,
                                confirmation_code=confirmation_code)
        send_confirmation_code(confirmation_code,
                               email=serializer.validated_data['email'])
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if confirmation_code == user.confirmation_code:
            token = str(AccessToken.for_user(user))
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        
        return Response(
            {'confirmation_code': ['Код не действителен']},
            status=status.HTTP_400_BAD_REQUEST
        )
