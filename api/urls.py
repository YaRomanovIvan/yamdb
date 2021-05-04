from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

router_v1 = DefaultRouter()
router_v1.register("categories", CategoryViewSet, basename="category")
router_v1.register("genres", GenreViewSet, basename="genre")
router_v1.register("titles", TitleViewSet, basename="title")
router_v1.register(
    prefix=r"titles/(?P<title_id>\d+)/reviews",
    viewset=ReviewViewSet,
    basename="api-reviews",
)
router_v1.register(
    prefix=r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    viewset=CommentViewSet,
    basename="api-comments",
)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
