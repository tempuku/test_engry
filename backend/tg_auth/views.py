from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AuthKeySerializer
from .services import TgTokenService


def home_view(request):
    """
    Renders the home page with a dynamic message depending on user authentication status.
    """
    context = {
        "user_message": f"Hi, {request.user.username}!"
        if request.user.is_authenticated
        else "Hi, anonymous!"
    }
    return render(request, "home.html", context)


def login_view(request):
    token = TgTokenService.get_new_token()
    html = render_to_string("popup.html", {"token": token})
    return JsonResponse(
        {
            "status": "ok",
            "html": html,
        }
    )


class AuthCheckView(APIView):
    """
    View to authenticate a user using a token (auth_key).
    """

    def post(self, request, *args, **kwargs):
        serializer = AuthKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_key = serializer.validated_data["auth_key"]  # pyright: ignore
        token = TgTokenService.validate_token(auth_key)
        if not token:
            return Response(
                {"status": "not_auth", "message": "Invalid token."},
                status=status.HTTP_200_OK,
            )
        user = TgTokenService.get_user_from_token(token)
        if not user:
            return Response(
                {
                    "status": "not_auth",
                    "message": "User does not exist or is inactive.",
                },
                status=status.HTTP_200_OK,
            )
        login(request, user)
        return Response({"status": "auth"}, status=status.HTTP_200_OK)
