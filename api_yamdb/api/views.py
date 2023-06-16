from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from rest_framework import viewsets, generics, status
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response

from reviews.models import Comment, Review, Title, User
from .permissions import (IsAdminOrModeratorOrOwnerOrReadOnly, AdminOrReadOnly,
                          IsAdmin)
from .serializer import ReviewSerializer, CommentSerializer
from .serializers import RegisterUserSerializer, TokenSerializer
from .send_util import send_confirm_code


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrOwnerOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        queryset = Review.objects.filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(
            title=title,
            author=self.request.user
        ).exists():
            raise ParseError
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all().order_by('id')

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


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
            confirmation_code = user.confirmation_code
        else:
            serializer.is_valid(raise_exception=True)
            User.objects.create(**serializer.validated_data,
                                confirmation_code=confirmation_code)
        send_confirm_code(confirmation_code,
                               email=serializer.validated_data['email'])
        return Response(data, status=status.HTTP_200_OK)


class GetTokenAPIView(generics.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if codegen.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        
        return Response(
            {'confirmation_code': ['Код не действителен']},
            status=status.HTTP_400_BAD_REQUEST
        )
