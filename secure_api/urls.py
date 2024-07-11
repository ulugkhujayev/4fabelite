from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Определение представления схемы API
schema_view = get_schema_view(
    openapi.Info(
        title="Безопасное API",
        default_version="v1",
        description="Безопасное и масштабируемое приложение Django API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@secureapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Определение URL-маршрутов приложения
urlpatterns = [
    path("admin/", admin.site.urls),  # Административная панель Django
    # URL-адреса API
    path("api/", include("users.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Swagger UI
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# Настройка кастомных обработчиков ошибок 404 и 500
handler404 = "secure_api.views.custom_404"
handler500 = "secure_api.views.custom_500"
