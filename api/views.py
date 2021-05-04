from django.db.models.aggregates import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from users.permissions import (
    IsAdminOrReadOnly,
    IsAuthor,
    IsModerator,
    IsReadOnly,
)

from .filters import ByReviewFilterBackend, ByTitleFilterBackend, TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .serializers import (
    CategorySerializers,
    CommentSerializer,
    GenreSerializers,
    ReviewSerializer,
    TitlePostSerializer,
    TitleSerializer,
)
from .utils import shortcut_get_review_or_404, shortcut_get_title_or_404


class CreateListDestroyViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    """
    A viewset that provides default `create()`, `destroy()`
    and `list()` actions.
    """

    pass


class TitleViewSet(ModelViewSet):
    """The view represent title and it's rating.

    The rating is calculated as average of reviews.
    """

    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")
    ).prefetch_related("genre", "category")

    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PATCH":
            return TitlePostSerializer
        return TitleSerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    lookup_field = "slug"


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    lookup_field = "slug"


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsModerator | IsAuthor | IsReadOnly,
    ]
    filter_backends = [ByTitleFilterBackend]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=shortcut_get_title_or_404(self),
        )


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsModerator | IsAuthor | IsReadOnly,
    ]
    filter_backends = [ByReviewFilterBackend]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=shortcut_get_review_or_404(self),
        )
