from django.http import JsonResponse


def custom_404(request, exception):
    return JsonResponse({"status_code": 404, "error": "Ресурс не найден"}, status=404)


def custom_500(request):
    return JsonResponse(
        {"status_code": 500, "error": "Внутренняя ошибка сервера"}, status=500
    )
