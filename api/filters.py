from django_filters import rest_framework as django_filters
from rest_framework import filters

from .models import Title
from .utils import shortcut_get_review_or_404, shortcut_get_title_or_404


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )
    genre = django_filters.CharFilter(
        field_name="genre",
        lookup_expr="slug",
    )

    category = django_filters.CharFilter(
        field_name="category",
        lookup_expr="slug",
    )

    class Meta:
        model = Title
        fields = [
            "year",
        ]


class ByTitleFilterBackend(filters.BaseFilterBackend):
    """Filter only objects that correspond to title_id.

    The Filter doesn't use related field to be more universal. There is a
    chance that it may be used in the future other views.
    """

    def filter_queryset(self, request, queryset, view):
        title = shortcut_get_title_or_404(view)
        return queryset.filter(title=title)


class ByReviewFilterBackend(filters.BaseFilterBackend):
    """Filter only objects that correspond to title_id and review_id.

    The Filter doesn't use related field to be more universal. There is a
    chance that it may be used in the future other views.
    """

    def filter_queryset(self, request, queryset, view):
        review = shortcut_get_review_or_404(view)
        return queryset.filter(review=review)
