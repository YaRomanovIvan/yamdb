from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import DRF_SUPPORT_EMAIL

from .permissions import IsAdmin
from .serializers import EmailSerializer, GetTokenSerializer, UserSerializer

User = get_user_model()


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
    }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path="me",
        url_name="personal_data",
    )
    def personal_data(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer_class()
            serializer_data = serializer(user)
        if request.method == "PATCH":
            serializer = self.get_serializer_class()
            serializer_data = serializer(user, data=request.data, partial=True)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
        return Response(serializer_data.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def api_mail(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data["email"]
    user, is_created = User.objects.get_or_create(email=email)
    confirmation_code = user.confirmation_code
    if is_created:
        user.is_active = False

    send_mail(
        subject="Код подтверждения",
        message=(f"Ваш код {confirmation_code} для получения токена"),
        from_email=DRF_SUPPORT_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    return Response(status=status.HTTP_200_OK)


class APIGetToken(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        code = serializer.data["confirmation_code"]
        user = get_object_or_404(User, email=email, confirmation_code=code)
        user.is_active = True
        return Response(get_token_for_user(user), status=status.HTTP_200_OK)
