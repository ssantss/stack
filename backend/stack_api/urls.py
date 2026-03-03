from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from stack_api.views import auth_config_view, google_auth_view, login_view, logout_view, me_view, refresh_view


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health_check),
    path("api/auth/config/", auth_config_view),
    path("api/auth/login/", login_view),
    path("api/auth/logout/", logout_view),
    path("api/auth/me/", me_view),
    path("api/auth/refresh/", refresh_view),
    path("api/auth/google/", google_auth_view),
]
