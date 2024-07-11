from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .serializers import UserSerializer
import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_permissions(self):
        if self.action == "create" or self.action == "verify_email":
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Создать нового пользователя",
        responses={201: UserSerializer()},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_verification_email(user)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"Создан новый пользователь: {user.email}")
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @swagger_auto_schema(
        operation_description="Подтвердить email пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "uidb64": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Base64 encoded user ID"
                ),
                "token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Verification token"
                ),
            },
        ),
        responses={
            200: "Email успешно подтвержден",
            400: "Недействительная ссылка для подтверждения",
        },
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def verify_email(self, request):
        uidb64 = request.data.get("uidb64")
        token = request.data.get("token")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            logger.info(f"Email подтвержден для пользователя: {user.email}")
            return Response(
                {"detail": "Email успешно подтвержден."}, status=status.HTTP_200_OK
            )
        else:
            logger.warning(
                f"Недействительная попытка подтверждения email для uidb64: {uidb64}"
            )
            return Response(
                {"detail": "Недействительная ссылка для подтверждения."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = f"{settings.SITE_URL}/verify-email/{uidb64}/{token}/"
        subject = "Подтвердите свой email"
        message = (
            f"Пожалуйста, перейдите по ссылке для подтверждения email: {verify_url}"
        )
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            logger.info(f"Отправлено письмо с подтверждением на email {user.email}")
        except Exception as e:
            logger.error(
                f"Не удалось отправить письмо с подтверждением на email {user.email}: {str(e)}"
            )

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"Создан пользователь: {user.email}")

    def perform_update(self, serializer):
        user = serializer.save()
        logger.info(f"Обновлен пользователь: {user.email}")

    def perform_destroy(self, instance):
        logger.info(f"Удален пользователь: {instance.email}")
        instance.delete()
