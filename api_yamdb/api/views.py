from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated)

from reviews.models import Category, Comment, Genre, Review, Title, User
from .permissions import (IsAdminOrModeratorOrOwnerOrReadOnly,
                          AdminOrReadOnly,
                          IsAdmin)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    ReadTitleSerializer
)
from .mixins import ListCreateDestroyViewSet, SearchFilterMixin
from .filters import TitleFilter
from users.serializers import UsersSerializer, UsersMeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("=username",)
    lookup_field = "username"
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            return (IsAdmin(),)
        return super().get_permissions()

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def get_patch_me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UsersMeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UsersMeSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrOwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        queryset = Review.objects.filter(title=title_id)
        return queryset


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


class CategoryViewSet(SearchFilterMixin, ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(SearchFilterMixin, ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadTitleSerializer
        return TitleSerializer
