from django.urls import include, path
from rest_framework import routers
from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    GetTokenAPIView,
    RegisterUserAPIView,
    ReviewViewSet,
    TitleViewSet,
)

app_name = 'api'

router_v1 = routers.DefaultRouter()


router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/'
    r'comments/(?P<comment_id>\d+)',
    CommentViewSet,
    basename='comment')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
    ReviewViewSet,
    basename='review')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)',
    TitleViewSet,
    basename='title')


auth_urls_v1 = [
    path('auth/signup/', RegisterUserAPIView.as_view(), name='signup'),
    path('auth/token/', GetTokenAPIView.as_view(), name='get_token'),
]

urlpatterns = [
    path('v1/', include(auth_urls_v1)),
    path('v1/', include(router_v1.urls)),
]
