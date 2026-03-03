from constance import config
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


COOKIE_OPTS = {
    "httponly": True,
    "samesite": "Lax",
    "secure": not settings.DEBUG,
}


def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


def set_auth_cookies(response, refresh):
    access_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
    refresh_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]

    response.set_cookie(
        "access_token",
        str(refresh.access_token),
        max_age=int(access_lifetime.total_seconds()),
        **COOKIE_OPTS,
    )
    response.set_cookie(
        "refresh_token",
        str(refresh),
        max_age=int(refresh_lifetime.total_seconds()),
        **COOKIE_OPTS,
    )
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def auth_config_view(request):
    return Response({
        "password": config.AUTH_PASSWORD_ENABLED,
        "google": config.AUTH_GOOGLE_ENABLED and bool(settings.GOOGLE_CLIENT_ID),
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    if not config.AUTH_PASSWORD_ENABLED:
        return Response(status=status.HTTP_404_NOT_FOUND)
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Usuario y contraseña son requeridos"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {"error": "Credenciales inválidas"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)
    response = Response({"user": serialize_user(user)})
    return set_auth_cookies(response, refresh)


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    response = Response({"detail": "Sesión cerrada"})

    raw_token = request.COOKIES.get("refresh_token")
    if raw_token:
        try:
            token = RefreshToken(raw_token)
            token.blacklist()
        except (InvalidToken, TokenError):
            pass

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(serialize_user(request.user))


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_view(request):
    token = request.COOKIES.get("refresh_token")
    if not token:
        return Response(
            {"error": "No hay refresh token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        refresh = RefreshToken(token)
        response = Response({"detail": "Token renovado"})
        return set_auth_cookies(response, refresh)
    except (InvalidToken, TokenError):
        return Response(
            {"error": "Refresh token inválido"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def google_auth_view(request):
    if not (config.AUTH_GOOGLE_ENABLED and settings.GOOGLE_CLIENT_ID):
        return Response(status=status.HTTP_404_NOT_FOUND)

    credential = request.data.get("credential")
    if not credential:
        return Response(
            {"error": "Token de Google requerido"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        idinfo = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError:
        return Response(
            {"error": "Token de Google inválido"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not idinfo.get("email_verified"):
        return Response(
            {"error": "Email de Google no verificado"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    email = idinfo["email"]
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=idinfo.get("given_name", ""),
            last_name=idinfo.get("family_name", ""),
        )
        user.set_unusable_password()
        user.save()

    refresh = RefreshToken.for_user(user)
    response = Response({"user": serialize_user(user)})
    return set_auth_cookies(response, refresh)
