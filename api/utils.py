from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Review, Title


def shortcut_get_title_or_404(view: ModelViewSet):
    title_id = view.kwargs.get("title_id")
    title = get_object_or_404(Title, id=title_id)
    return title


def shortcut_get_review_or_404(view: ModelViewSet):
    title_id = view.kwargs.get("title_id")
    review_id = view.kwargs.get("review_id")
    review = get_object_or_404(
        Review,
        id=review_id,
        title__id=title_id,
    )
    return review
