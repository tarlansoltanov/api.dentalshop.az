from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView, TokenVerifyView

from server.apps.authentication.logic.serializers import AccessTokenSerializer, RegisterSerializer, TokenPairSerializer
from server.apps.core.logic.responses import BAD_REQUEST, FORBIDDEN, UNAUTHORIZED


class AdminLoginView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials for admin.
    """

    @extend_schema(
        responses={
            status.HTTP_200_OK: TokenPairSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: FORBIDDEN,
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.user.is_staff:
            return Response({"detail": "You don't have permission to login!"}, status=status.HTTP_403_FORBIDDEN)
        return super().post(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    """
    Takes a set of user credentials and creates a new user account.
    """

    serializer_class = RegisterSerializer

    @extend_schema(
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

    @extend_schema(
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

    @extend_schema(
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

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
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

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Token is blacklisted",
            ),
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
