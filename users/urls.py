from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "users/verify-email/",
        UserViewSet.as_view({"post": "verify_email"}),
        name="verify_email",
    ),
]
