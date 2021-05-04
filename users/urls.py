from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIGetToken, UserViewSet, api_mail

router = DefaultRouter()
router.register("users", UserViewSet)

auth_urls = [
    path("email/", api_mail),
    path("token/", APIGetToken.as_view()),
]

urlpatterns = [
    path("v1/auth/", include(auth_urls)),
    path("v1/", include(router.urls)),
]
