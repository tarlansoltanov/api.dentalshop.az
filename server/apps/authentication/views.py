from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView, TokenVerifyView

from server.apps.authentication.logic.serializers import AccessTokenSerializer, RegisterSerializer, TokenPairSerializer
from server.apps.core.logic.responses import BAD_REQUEST, UNAUTHORIZED


class RegisterView(generics.CreateAPIView):
    """
    Takes a set of user credentials and creates a new user account.
    """

    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: RegisterSerializer,
            status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenPairSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: AccessTokenSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VerifyView(TokenVerifyView):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Token is valid",
            ),
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(TokenBlacklistView):
    """
    Takes a refresh type JSON web token and adds it to the blacklist if the
    token is valid. Once blacklisted, the token cannot be used to obtain a new
    access type JSON web token or to refresh an existing access type JSON web
    token.
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Token is blacklisted",
            ),
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
